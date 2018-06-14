class Location {

    constructor() {
        this.enable_flg = false;
        this.position = null
        this.geolocation = null;
        this.__cheakEnable();
    }

    // httpsじゃないと使えなくなってる模様
    __cheakEnable() {
        try {
            if (typeof (navigator.geolocation) == 'undefined') {
                this.geolocation = google.gears.factory.create('beta.geolocation');
            } else {
                this.geolocation = navigator.geolocation;
            }
        } catch (e) { 
            console.log(e);
        }
        this.enable_flg = this.geolocation != null;
    }

    isEnable() {
        return this.enable_flg;
    }

    getGeolocation(){
        return this.geolocation;
    }

    setPosition(position){
        this.position = position;
    }
    getPosition(position){
        return this.position;
    }

    setLocation() {
        navigator.geolocation.watchPosition(
            // 成功
            (position) => {
                this.position = position;
                //   '<td>' + position.coords.latitude + '</td>' +
                //   '<td>' + position.coords.longitude + '</td>' +
                //   '<td>' + position.coords.altitude + '</td>' +
                //   '<td>' + position.coords.accuracy + '</td>' +
                //   '<td>' + position.coords.altitudeAccuracy + '</td>' +
                //   '<td>' + position.coords.heading + '</td>' +
                //   '<td>' + position.coords.speed + '</td>' +
                //   '<td>' + position.timestamp + '</td>' +
            },
            // エラーコードのメッセージを定義
            (error) => {
                this.enable_flg = false;
                // var errorMessage = {
                //     0: "原因不明のエラーが発生しました…。" ,
                //     1: "位置情報の取得が許可されませんでした…。" ,
                //     2: "電波状況などで位置情報が取得できませんでした…。" ,
                //     3: "位置情報の取得に時間がかかり過ぎてタイムアウトしました…。" ,
                // } ;
                // alert( errorMessage[error.code] ) ;
            },
            // オプション
            {
                "enableHighAccuracy": false,
                "timeout": 1000000,
                "maximumAge": 0,
            }
        );
    }

    getDistanceOfKm(latitude, longitude) {
        if (!this.enable_flg) return;
        let radians = (deg)=>{
            return deg * Math.PI / 180;
        }
        const lat1 = this.position.coords.latitude;
        const lng1 = this.position.coords.longitude;
        const lat2 = latitude;
        const lng2 = longitude;
        return 6378.14 * Math.acos(Math.cos(radians(lat1)) *
            Math.cos(radians(lat2)) *
            Math.cos(radians(lng2) - radians(lng1)) +
            Math.sin(radians(lat1)) *
            Math.sin(radians(lat2)));
    }

}
// export default new Location()

import Vue from 'Vue';

export default new Vue({
    data: {
        // Jsonデータ格納用
        is_enable: false,
        position: null
    },
    created(){
        this.obj = new Location();
        this.is_enable = this.obj.isEnable();
    },
    methods: {
        set_location(){
            this.obj.getGeolocation().watchPosition(
                // 成功
                (position) => {
                    Vue.set(this, 'position', position);
                    this.obj.setPosition(position);
                    this.$emit('GET_LOCATION_POSITION');
                },
                // エラーコードのメッセージを定義
                (error) => {
                    console.log(error);
                    this.enable_flg = false;
                    Vue.set(this, 'is_enable', false);
                    this.$emit('GET_LOCATION_POSITION');
                },
                // オプション
                {
                    "enableHighAccuracy": false,
                    "timeout": 1000000,
                    "maximumAge": 0,
                }
            );
        },
        get_location(){
            return this.obj.getPosition()
        },
        get_distance(latitude, longitude){
            return this.obj.getDistanceOfKm(latitude, longitude)
        }
    }
})
