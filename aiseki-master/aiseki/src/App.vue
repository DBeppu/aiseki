<template>
  <div id="app">
    <header>
      <div class="wrapper clearfix">
          <div class="logo float-left"><a href="/"><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/logo-wh.png" class="img-fluid"></a></div>
          <div class="leadcopy float-right"><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/head-copy.png" class="img-fluid"></div>
      </div>
    </header>

    <router-view/>

    <footer>
      <p>&copy; reservele</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
