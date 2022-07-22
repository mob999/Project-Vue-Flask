<template>
  <div id="app">
    <image-container/>
  </div>
</template>

<script>
import ImageContainer from './components/ImageContainer.vue'
export default {
  name: 'App',
  components: {
    'image-container': ImageContainer
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  height: 1200px;
  width: 80%;
  margin-left: 10%;
  margin-right: 10%;
}
* {
  margin: 0;
}
</style>
