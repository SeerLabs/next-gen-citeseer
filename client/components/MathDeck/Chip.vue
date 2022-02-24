<template>
  <ChipDisplay
    :id="id"
    :key="id"
    :containerStyle="{
      'left': x + 'px',
      'top': y + 'px',
      'z-index': isActive ? '12' : null,
    }"
    :onClick="singleDoubleClick"
    :color="isFresh ? 'blue' : 'darkgrey'"
    :chipStyle="chipStyle"
    :onDragStart="dragStart"
    :onDragEnd="dragEnd"
    :onDragEnter="dragEnter"
    :onDragLeave="dragLeave"
    :title="chipStr"
    @pointerup.stop
    @pointerdown.stop
    @wheel="wheelScaling"
  >
    <!-- <img v-if="imageData" :src="imageData" id="download-img"> -->
    <span v-if="symbolIds" style="color: black;" >
      <MathSymbolCollection
        :bbox="{
          width: 'auto',
          height: chipHeight,
          }"
        :symbolIds="symbolIds" />
    </span>
    <span v-else v-html="chipStr"></span>

  </ChipDisplay>
</template>

<script>
import _ from 'lodash';
import ChipDisplay from './ChipDisplay';
import MathSymbolCollection from './MathSymbol/Collection';
import { mixin } from '@/store/mixin';
import {
  ScriptEditor as SE,
  EditorModes as EM,
} from '@/editor';
import { SvgOps } from '@/svg-operations';

const colors = require('vuetify/es5/util/colors');

export default {
  name: 'Chip',
  props: {
    id: Number,
    onClick: {
      type: Function,
      default: () => {},
    },
    insertionMode: {
      Type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      clicks: 0,
      imageData: '',
      imageDataTimeout: null,
    };
  },
  components: {
    ChipDisplay,
    MathSymbolCollection,
  },
  mixins: [mixin],
  computed: {
    chip() {
      return this.getChip(this.id) || {};
    },
    isFresh() {
      return this.chip.isFresh;
    },
    isFavorite() {
      const chipGroupObj = this.chipStr === '' && this.symbolIds.length > 0
        ? this.chipGroups[this.toSymbolStr(this.id)] : this.chipGroups[this.chipStr];
      return !!(chipGroupObj || {}).favoriteId;
    },
    filename() {
      const time = new Date().toLocaleTimeString().replace(' ', '');
      const date = new Date().toLocaleDateString().replace(' ', '');
      let today = `${date}_${time}`;

      // Strip away escaped characters
      today = today.replace(/[^\w\s]/gi, '');

      return `mathdeck_formula_${today}.jpg`;
    },
    symbolIds() {
      // // Also display selected symbols if this is the active formula
      // if (this.isActiveFormula && this.selectedSymbols.length) {
      //   return [...this.chip.symbolIds, ...this.selectedSymbols];
      // }
      return this.chip.symbolIds;
    },
    x() {
      return this.chip.x - (this.isTemplate
        ? SE.templateChipPadding.left
        : SE.chipPadding.left);
    },
    y() {
      return this.chip.y - (this.isTemplate
        ? SE.templateChipPadding.top
        : SE.chipPadding.top);
    },
    chipHeight() {
      return this.chip.height || 30;
    },
    chipStr() {
      return this.chip.str;
    },
    symbols() {
      return this.symbolIds.map(this.getSymbol);
    },
    symbolsLength() {
      return this.symbolIds.length;
    },
    chipSVG() {
      return this.getChipSVG(this.id) || {};
    },
    isActive() {
      return this.activeChip === this.id;
    },
    isActiveFormula() {
      return this.activeFormulaId === this.id;
    },
    chipStyle() {
      return {
        background: this.background,
        borderStyle: 'solid',
        borderColor: this.borderColor,
        borderWidth: this.borderWidth,
        padding: this.isActiveFormula ? '4px' : '0px',
        margin: this.chipMargin,
      };
    },
    chipDisplay() {
      return this.$refs.chipDisplay;
    },
    chipMargin() {
      if (this.insertionMode) {
        return '3px';
      }
      if (!this.isFresh) {
        return '2px';
      }
      return '0px';
    },
    borderWidth() {
      if (this.isActiveFormula) {
        return '6px';
      }
      if (this.insertionMode) {
        return '0';
      }
      if (!this.isFresh) {
        return '1px';
      }
      return '3px';
    },
    borderColor() {
      if (this.id === this.duplicateChipId) {
        return 'red !important';
      }
      if (!this.isFresh || this.insertionMode) {
        return 'darkgrey !important';
      }
      if (this.isFavorite) {
        return `${colors.default.amber.accent4} !important`;
      }
      return this.style.formulaBlue;
    },
    background() {
      if (this.insertionMode) {
        return '#f5f5f5 !important';
      }
      if (!this.isFresh && this.isFavorite) {
        return '#FFAB0040 !important';
      } if (!this.isFresh) {
        return '';
      } return '#f0f0f0 !important';
    },
    isTemplate() {
      return !!this.chip.isTemplate;
    },
    // symbolsBBox() {
    //   return SvgOps.getBBox(...this.symbols);
    // },
    // symbolsString() {
    //   return JSON.stringify(this.symbols);
    // },
  },
  watch: {
    // symbolsString: {
    //   // immediate: true,
    //   handler() {
    //     this.debounceImageUpdate();
    //   },
    // },
    // filename() {
    //   this.debounceImageUpdate();
    // },
    // x() {
    //   console.log(this.id, this.$refs);
    // },
  },
  mounted() {
    // Initialize images after short delay
    // setTimeout(this.debounceImageUpdate, 100);
  },
  methods: {
    async showControls() {
      // If right clicking on the same entity chip,
      // then simply toggle the state of entityActive
      if (this.entityActiveChip === this.id) {
        this.entityActive = !this.entityActive;
      } else {
        // right clicking on a different entity chip
        // Always show the entity popper.
        this.entityActive = true;
      }
      // Update the entityChipActive
      this.entityActiveChip = this.id;
    },
    wheelScaling(e) {
      if (!this.chip.isHistory && this.isChipOnCanvas(this.id)) {
        const scrollDown = e.deltaY > 0;
        this.scaleChipHeight(
          this.id,
          1.1 ** (scrollDown ? -2 : 2),
        );
      }
    },
    async updateImageData() {
      try {
        if (this.imageData) {
          window.URL.revokeObjectURL(this.imageData);
        }
        this.imageData = await this.generateImage();
      } catch (e) {
        console.log(e);
      }
    },
    // // Update the chip image after 0.3s has elapsed.
    // // Once the image is updated, clear the timeout.
    // // If called again within interval, it will clear
    // // and restart the timeout
    // debounceImageUpdate() {
    //   if (this.imageDataTimeout) {
    //     clearTimeout(this.imageDataTimeout);
    //   }

    //   this.imageDataTimeout = setTimeout(() => {
    //     this.updateImageData();
    //     this.imageDataTimeout = null;
    //   }, 300);
    // },
    singleDoubleClick() {
      this.clicks += 1;
      setTimeout(() => {
        if (this.clicks >= 2) {
          this.clicks = 0;
          this.dropToCanvas();
        } else if (this.clicks === 1) {
          this.clicks -= 1;
        } else {
          // This shouldn't happen
          this.clicks = 0;
        }
      }, 500);
    },
    dragStart(ev) {
      this.controlsActive = false;
      this.mode = EM.select;
      // eslint-disable-next-line no-param-reassign
      ev.dataTransfer.effectAllowed = 'copy';
      const chip = ev.target.closest('.chip');
      const chipContent = chip.childNodes[0];
      const container = chip.closest('.chip-container');
      const originalIndex = Array.prototype.indexOf.call(
        container.parentElement.children,
        container,
      );
      const collectionId = container.parentNode.id;
      container.dataset.originalIndex = originalIndex;
      container.dataset.collectionId = collectionId;

      const cRect = chip.getBoundingClientRect();
      this.draggingChip = this.id;
      const data = {
        chipId: this.id,
        chipSelector: `#chip-id-${this.id}`,
        offsetX: ev.clientX - cRect.x,
        offsetY: ev.clientY - cRect.y,
        latex: this.chipStr,
        isFresh: this.isFresh,
        chipData: this.chip,
      };
      ev.dataTransfer.setData('text/plain', JSON.stringify(data));
      ev.dataTransfer.setDragImage(chipContent, ev.clientX - cRect.x, ev.clientY - cRect.y);
    },
    async dragEnd(ev) {
      this.draggingChip = null;
      const container = this.getChipContainerEl(this.id);
      if (!container) return;
      container.classList.remove('dragged-chip');

      // Fix element position if reorder was cancelled by ending the
      // drag outside of the collection
      const overEl = document.elementFromPoint(ev.clientX, ev.clientY);

      if (overEl === null) {
        return;
      }

      const { collectionId, originalIndex } = container.dataset;
      // If chip is not in its original collection
      if (!collectionId || !overEl.closest(`#${collectionId}`)) {
        const collection = container.parentElement;
        const currentIndex = Array.prototype.indexOf.call(
          collection.children,
          container,
        );
        const positionEl = (currentIndex > originalIndex)
          ? collection.children.item(originalIndex)
          : collection.children.item(originalIndex).nextSibling;

        collection.insertBefore(container, positionEl);
      }
      delete container.dataset.collectionId;
      delete container.dataset.originalIndex;
    },
    dragEnter() {
      // console.log('dragenter');
      // console.log(e);
    },
    dragLeave() {
      // console.log('dragleave');
      // console.log(e);
    },
    dropToCanvas() {
      if (this.isChipOnCanvas(this.id)
        // Don't allow dropping the active formula
        && !this.isActiveFormula
      ) {
        this.dropChipSymbolsToCanvas(this.id);
      }
    },
    async generateImage() {
      if (!this.symbolsLength) {
        return null;
      }

      const symbols = _.cloneDeep(this.symbols).map(s => ({
        ...s,
        id: undefined,
        attributes: {
          ...s.attributes,
          x: s.attributes.x - this.symbolsBBox.x,
          y: s.attributes.y - this.symbolsBBox.y,
        },
      }));

      const { imageURL } = await SvgOps.toBase64Image(
        symbols,
        'image/jpeg',
        this.chip,
        this.filename,
      );

      return imageURL;
    },
  },
};
</script>
<style>

  .chip-history-card{
    max-width: 50%;
    display: flex;
    width: 50%;
    min-height: 70%;
  }

  #download-img {
    opacity: 0;
    width: 100%;
    height: 100%;
    position: absolute;
  }

  .chip .v-chip__content {
    position: relative;
  }

</style>
