<template>
  <div id="main" class="list">
    <div class="wrapper">
        <p class="bread-crumb">
            <router-link :to="{ path: '/' }">TOP</router-link> / 
            <a v-on:click="change_area(area_parent, '')">{{area_parent?area_parent:'未選択'}}</a> / 
            {{area_child?area_child:'未選択'}}</p>
        <p class="result">{{count}}件を検索</p>

        <section v-for="v in list" class="shop-list">
            <p class="name">
                <router-link :to="{ path: 'item', query: {id:v.id,area_parent:area_parent,area_child:area_child} }">{{v.name}}</router-link>
            </p>
            <p class="address">{{v.address}}</p>
            <p class="tel">TEL : <a :href="'tel:'+ v.tel">{{v.tel}}</a></p>
            <div class="number clearfix" v-if="v.id in visitors">
                <div class="men float-left">
                    <p><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/pict_men.png" width="auto" height="24">{{visitors[v.id]['men']}}<small>{{visitors[v.id]['type']}}</small></p>
                </div>
                <div class="women float-right">
                    <p><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/pict_women.png" width="auto" height="24">{{visitors[v.id]['women']}}<small>{{visitors[v.id]['type']}}</small></p>
                </div>
            </div>
        </section>
    </div>
</div>
</template>

<style>
.bread-crumb a:not([href]):not([tabindex]){
    color: #007bff;
}
</style>


<script>
import api from "../api";

export default {
  name: 'List',
  data () {
    return {
      list_all:[],
      list:[],
      visitors:{},
      count:0,
      area_parent:this.$route.query.area_parent,
      area_child:this.$route.query.area_child
    }
  },
  created() {
    // Json取得
    api.get_static_json('aiseki.json', 'aiseki');
    api.get_static_json('visitor.json', 'visitor');
    // Json取得後に呼び出される
    api.$on('GET_STATIC_JSON_COMPLETE', () => {
      this.list_all = api.get_data('aiseki');
      let visitors = api.get_data('visitor');
      this.visitors = {};
      visitors.forEach((v)=>{
          this.visitors[v.aiseki_id] = v;
      });
      this.filter();
    });
  },
  methods:{
      filter(){
        if(this.area_parent){
            this.list = this.list_all.filter((val)=>{
                return (val.area == this.area_parent && (!this.area_child || val.area_detail == this.area_child))
            });
        }
        this.count = this.list.length;
      },
      change_area(area_parent, area_child){
          this.area_parent = area_parent;
          this.area_child = area_child;
          this.filter();
      }
  }
}
</script>