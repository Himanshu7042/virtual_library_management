<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
  props: {
    pieData: {
      type: Array,
      required: true
    }
  },
  watch: {
    pieData: {
      immediate: true, // Run the handler immediately on component mount
      handler(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.drawChart();
        }
      }
    }
  },
  methods: {
    async drawChart() {
      try {
        const data = this.pieData;

        const width = 400;
        const height = 400;
        const radius = Math.min(width, height) / 2;

        // Remove existing SVG before redrawing
        d3.select(this.$refs.chart).select("svg").remove();

        const svg = d3.select(this.$refs.chart)
          .append("svg")
          .attr("width", width)
          .attr("height", height)
          .append("g")
          .attr("transform", `translate(${width / 2},${height / 2})`);

        const color = d3.scaleOrdinal()
          .domain(data.map(d => d.label))
          .range(d3.schemeCategory10);

        const pie = d3.pie()
          .value(d => d.value);

        const arc = d3.arc()
          .innerRadius(0)
          .outerRadius(radius);

        const arcs = svg.selectAll(".arc")
          .data(pie(data))
          .enter()
          .append("g")
          .attr("class", "arc");

        arcs.append("path")
          .attr("fill", d => color(d.data.label))
          .attr("d", arc);

        arcs.append("text")
          .attr("transform", d => `translate(${arc.centroid(d)})`)
          .attr("text-anchor", "middle")
          .text(d => d.data.label);
      } catch (error) {
        console.error('Error drawing pie chart:', error);
      }
    }
  },
  async mounted() {
    // Call drawChart initially when the component mounts
    await this.drawChart();
  }
};
</script>

<style scoped>
/* Add styles if needed */
</style>
