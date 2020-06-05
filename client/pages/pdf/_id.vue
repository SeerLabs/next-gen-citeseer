<template>
    <div>
        <pdf src="http://localhost:8000/api/document?repid=rep1&type=pdf&doi=10.1.1.1028.1"></pdf>
    </div>
</template>
 
<script>
import pdf from 'vue-pdf'
 
export default {
  components: {
    pdf
  }
}
</script>