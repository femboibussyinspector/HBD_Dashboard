// import { chartsConfig } from "@/configs";
import { chartsConfig } from "../configs/charts-config";

const dataScrapped = {
  type: "bar",
  height: 220,
  series: [
    {
      name: "Scraped Data",
      data: [700, 900, 1800],
    },
  ],
  options: {
    ...chartsConfig,
    colors: "#388e3c",
    plotOptions: {
      bar: {
        columnWidth: "16%",
        borderRadius: 5,
      },
    },
    xaxis: {
      ...chartsConfig.xaxis,
      categories: ["D-Mart", "Amazon", "Google Map"],
      labels: {
        formatter: function(val) {
          if(window.innerWidth < 480){
            const mapping = {
              "D-Mart": "DM",
              "Amazon": "DM",
              "Google Map": "G-Map",
            };
            return mapping[val] || val;
          }
          return val;
        }
      },
    },
  },
};

const scrappingTrend = {
  type: "line",
  height: 220,
  series: [
    {
      name: "Scraped Data",
      data: [700, 900, 1800],
    },
  ],
  options: {
    ...chartsConfig,
    colors: ["#0288d1"],
    stroke: {
      lineCap: "round",
    },
    markers: {
      size: 5,
    },
    xaxis: {
      ...chartsConfig.xaxis,
      categories: ["D-Mart", "Amazon", "Google Map"],
      labels: {
        formatter: function(val) {
          if(window.innerWidth < 480){
            const mapping = {
              "D-Mart": "DM",
              "Amazon": "DM",
              "Google Map": "G-Map",
            };
            return mapping[val] || val;
          }
          return val;
        }
      },
    },
  },
};

const categoriesData = {
  type: "pie",
  height: 268,
  series: [700, 300, 400], // Product, Listing, Others
  options: {
    chart: {
      fontFamily: "inherit",
    },
    labels: ["Product", "Listing", "Others"],
    colors: ["#EF4444", "#10B981", "#8B5CF6"],

    // 1. Plot Options (Text ko position set karne k liye)
    plotOptions: {
      pie: {
        dataLabels: {
          offset: -8,
          minAngleToShowLabel: 10,
        },
      },
    },

    // 2. DataLabels (Percentage Text)
    dataLabels: {
      enabled: true,
      style: {
        fontSize: "12px",
        fontWeight: 500,
        colors: ["#ffffff"],
        fontFamily: "inherit",
        shadow: {
        top: 1,
        left: 1,
        blur: 2,
        color: "#000",
        opacity: 0.5,
      },
      },
    },

    legend: {
      show: true,
      position: "bottom",
      fontSize: "13px",
      fontWeight: 400,
      itemMargin: {
        horizontal: 10,
        vertical: 5,
      },
      onItemHover: {
        highlightDataSeries: true
      },
    },

    // 4. Tooltip (Hover effect)
    tooltip: {
      theme: "light",
      fillSeriesColor: false,
      style: {
        fontSize: "13px",
        fontFamily: "inherit",
        color: "#333",
      },
      marker: {
        show: true,
      },
      y: {
        formatter: function (val) {
          return val;
        },
      },
    },
  },
};


export const statisticsChartsData2 = [
  {
    color: "white",
    title: "Source-wise Data Scraped",
    description: "Last Campaign Performance",
    footer: "campaign sent 2 days ago",
    chart: dataScrapped,
  },
  {
    color: "white",
    title: "Scraping Trend",
    description: "Last Campaign Performance",
    footer: "just updated",
    chart: scrappingTrend,
  },
  {
    color: "white",
    title: "Categories Distribution",
    description: "Last Campaign Performance",
    footer: "just updated",
    chart: categoriesData,
  },
];

export default statisticsChartsData2;