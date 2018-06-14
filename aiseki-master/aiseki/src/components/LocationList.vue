<template>
  <div id="main" class="list">
    <div class="wrapper">
        <p class="bread-crumb">
            <router-link :to="{ path: '/' }">TOP</router-link> / 現在位置</p>
        
        <p class="loading" v-if="!end_load"><img src="/reservele-aiseki/static/images/loading.gif"></p>
        <p class="result" v-if="end_load">{{count}}件を検索</p>

        <section v-for="v in list" class="shop-list">
            <p class="name">
                <router-link :to="{ path: 'item', query: {id:v.id} }">{{v.name}}</router-link>
            </p>
            <p class="address">{{v.address}}</p>
            <p class="tel">TEL : <a :href="'tel:'+ v.tel">{{v.tel}}</a></p>
            <div class="number clearfix">
                <div class="men float-left">
                    <p><img src="/static/images/pict_men.png" width="auto" height="24">30<small>people</small></p>
                </div>
                <div class="women float-right">
                    <p><img src="/static/images/pict_women.png" width="auto" height="24">30<small>people</small></p>
                </div>
            </div>
        </section>
    </div>
</div>
</template>

<style>
.loading{
    text-align: center;
}
</style>

<script>
import api from "../api";
import gps from "../location";

export default {
  name: 'LocationList',
  data () {
    return {
      list_all:[],
      list:[],
      count:0,
      end_load:false,
    }
  },
  created() {
    gps.set_location();
    // Json取得
    api.get_static_json('aiseki.json', 'aiseki');
    // Json取得後に呼び出される
    api.$on('GET_STATIC_JSON_COMPLETE', () => {
      this.list_all = api.get_data('aiseki');
        if(gps.get_location()){
            this.filter();
        }else{
            gps.$on('GET_LOCATION_POSITION',this.filter);
        }
    });
    
  },
  methods:{
      filter(){
        this.list_all = this.list_all.filter((val)=>{
            const distance = gps.get_distance(val.latitude, val.longitude);
            return distance < 5;
        });
        this.list = this.list_all;
        this.count = this.list.length;   
        this.end_load = true;
      }
    }
}
</script>