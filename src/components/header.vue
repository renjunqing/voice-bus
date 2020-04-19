<template>
  <div class="page-header">
    <div v-if="showBack" class="back" @click="$router.go(-1)"></div>
    <div class="title">{{title}}</div>
    <div class="right-icon">
      <slot name="rightIcon"></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showBack: {
      type: Boolean,
      default: true,
    },
    title: {
      type: String,
      default: '语音公交'
    }
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .page-header {
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    line-height: .5rem;
    color: #fff;
    text-align: center;
    background: #1abc9c;
  }
  .back {
    background-image: url(assets/icons8-back-32.png);
    width: .3rem;
    height: .3rem;
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    background-size: contain;
  }
  .right-icon {
    width: .3rem;
    height: .3rem;
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background-size: contain;
  }
  .title {
    font-size: .18rem;
  }
</style>
