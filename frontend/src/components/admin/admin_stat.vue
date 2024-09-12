<template>
    <div class="container">
      <div class="left-chart">
        <h2>Book Name wise book issue</h2>
        <BarChart :barData="barData" />
      </div>
      <div class="right-chart">
        <h2>Section wise book issue</h2>
        <PieChart :pieData="pieData" />
      </div>
    </div>
  </template>
  
  <script>
  import PieChart from './PieChart.vue';
  import BarChart from './BarChart.vue';
  import axiosFetch from '../../axios';
  
  export default {
    components: {
      PieChart,
      BarChart
    },
    data() {
      return {
        pieData: [],
        barData: []
      };
    },
    mounted() {
      // Fetch data from API
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          // Fetch pie data
          const pieResponse = await axiosFetch.get(`/pie`);
          this.pieData = pieResponse.data;
  
          // Fetch bar data
          const barResponse = await axiosFetch.get(`/bar`);
          this.barData = barResponse.data;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
  }
  
  .left-chart, .right-chart {
    flex: 1;
    margin: 0 20px;
  }
  
  h2 {
    text-align: center;
  }
  </style>
  