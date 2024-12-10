<template>
  <div class="hello">
    <div>
     <p>teste</p>
     <img  :src="foto" width="200" height="260">
    </div>
    <div>
     <p>teste 2</p>
     <img  :src="imageformData" width="200" height="260">
    </div>
  </div>
</template>

<script>

import imagem from '../assets/ian.jpg'  

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },

  data(){
    return{
      foto: imagem, 
      imageformData: '',
    }
  },
  
  mounted(){
    this.formatImg()
  },
  
  methods: {

    formatImg(){

      let image = this.foto

      let formData = new FormData()
      formData.append('file', image[0])

      console.log(' formData ', formData)

      // this.axios.get(api).then((response) => {
      //   console.log(response.data)
      // })

      // const formData = new FormData();
      // let imag = formData.append('image', image.files);
      // console.log(' image -;--> ', image)

      // this.imageformData = imag 

    }
    
  }

}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
