
var app = getApp()

Page({
  data: {
    indicatorDots: true,
    autoplay: true,
    interval: 2000,
    duration: 500,
    imgUrls: [],
    list:[]
  },

  onLoad: function(options) {
    this.loadData()
  },

  loadData: function() {
    
  },

  onPullDownRefresh: function() {
    this.loadData()
  },
  
})