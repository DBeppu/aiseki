<template>
<div id="main" class="top">
    <div class="wrapper">
        <h1 class="head"><img src="https://s3-ap-northeast-1.amazonaws.com/reservele-aiseki/static/images/logo.png" class="img-fluid" alt="相席サーチ" title="相席サーチ"></h1>
        <div class="head text-center">
            <p>エリアで探す</p>
        </div>
        <div class="select_area">
          <label>
          <select name="area_parent" v-model="selected_p_area" ref="area_parent" class="select_area">
              <option value="" disabled selected>都道府県</option>
              <option v-for="(v,k) in area_list" v-bind:value="k">{{k}}</option>
          </select>
          </label>
        </div>
        <div class="select_area">
          <label>
          <select name="area_child" v-model="selected_c_area" ref="area_child" class="select_area">
              <option value="" disabled selected>市区町村</option>
              <option value=""></option>
              <option v-for="v in area_list[selected_p_area]">{{v}}</option>
          </select>
          </label>
        </div>
        <p><a v-on:click="to_list(selected_p_area, selected_c_area)" class="btn-round">上記のエリアで探す</a></p>
        <hr v-if="enable_gps">
        <p v-if="enable_gps">
          <router-link :to="{ path: '/lolist' }" class="btn-round" role="button">現在地から探す</router-link>
        </p>
    </div>
</div>
</template>

<style>
.select_area{
    width: 100%;
}
.select_area select {
    text-align: center;
    text-align-last: center;
    position: relative;
    width: 100%;
    padding: 10px;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    border: none;
    background: #fff;
    color:#BBB;
    font-size:1.2em;
    border-radius: 0;
}
.select_area option {
  text-align: left;
}
.select_area label {
	position: relative;
  width: 100%;
  line-height: 40px;
}
 
.select_area label:after {
	display: block;
	content: " ";
	position: absolute;
	top: 50%;
	right: 20px;
	width: 20px;
	height: 20px;
	margin-top: -8px;
  background: url('/reservele-aiseki/static/images/chevron-bottom.svg') 0 0 no-repeat;
	background-size: 15px;
	pointer-events: none;
}
.select_area.selected_font_color{
  color:#000;
}
select:required:invalid {
  color: gray;
}
option[value=""][disabled],option[disabled]{
  display: none;
}
option {
  color: black;
}
</style>

<script>

import api from "../api";
import gps from "../location";
import router from '../router'

export default {
  name:'Index',
  data() {
    return {
      // Jsonのデータを格納
      area_list: [],
      selected_p_area: "",
      selected_c_area: "",
      enable_gps:false,
    };
  },
  created() {
    // Json取得
    api.get_static_json('area.json', 'area');

    api.$on('GET_STATIC_JSON_COMPLETE', () => {
      this.area_list = api.get_data('area')
    });
    this.enable_gps = gps.is_enable
  },
  updated(){
      this.$refs['area_parent'].onchange = ()=>{
        if(this.$refs['area_parent'].value){
          this.$refs['area_parent'].classList.add("selected_font_color")
        }else{
          this.$refs['area_parent'].classList.remove("selected_font_color")
        }
      }
      this.$refs['area_child'].onchange = ()=>{
        if(this.$refs['area_child'].value){
          this.$refs['area_child'].classList.add("selected_font_color")
        }else{
          this.$refs['area_child'].classList.remove("selected_font_color")
        }
      }
  },
  methods:{
    to_list(area_parent, area_child){
      if(!area_parent)return;
      router.push({ path: '/list', query: {area_parent:area_parent,area_child:area_child}})
    }
  }
}
</script>