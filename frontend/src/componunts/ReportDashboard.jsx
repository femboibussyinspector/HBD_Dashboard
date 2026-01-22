import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Card,
  CardBody,
  Typography,
  Button,
} from "@material-tailwind/react";
import {
  ArchiveBoxIcon,
  MapPinIcon,
  TagIcon,
  ArrowLongRightIcon,
  ServerStackIcon,
  GlobeAmericasIcon,
  ChartBarIcon,
  ClockIcon,
} from "@heroicons/react/24/solid";
import SlotCounter from "react-slot-counter";

import api from "../utils/Api";

import {StatisticsChart} from "../widgets/charts/statistics-chart";
import statisticsChartsData2 from "../data/statistics-charts-data2";

export function ReportDashboard() {
  const [stats, setStats] = useState({
    productCount: 0,
    cityCount: 0,
    categoryCount: 0,
    loading: true,
  });
  
  const staticData = {
    totalScrapped: 1200000,
  };

  useEffect(() => {
    const fetchProductsData = async () => {
      try {
        const response = await api.get("/googlemap_data");
        const products = response.data;

        const uniqueCities = new Set(products.map((p) => p.city)).size;
        const uniqueCategories = new Set(products.map((p) => p.category)).size;

        setStats({
          productCount: products.length,
          cityCount: uniqueCities,
          categoryCount: uniqueCategories,
          loading: false,
        });
      } catch (error) {
        console.error("error fetching products:", error);
        setStats((prev) => ({ ...prev, loading: false }));
      }
    };

    fetchProductsData();
  }, []);

  const DashboardCard = ({ title, value, icon: Icon, color, link, subValue }) => (
    <Card className="relative overflow-hidden border border-gray-200 bg-gradient-to-br from-white to-gray-500/30 shadow-md transition-all hover:shadow-md hover:-translate-y-3 duration-300">
      <CardBody className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <Typography variant="h5" color="blue-gray" className="mb-1 font-bold tracking-tight">
              {title}
            </Typography>
            <Typography className="font-normal text-gray-500 text-sm">
              {subValue || "real-time updates"}
            </Typography>
          </div>
          <div className={`flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${color} shadow-md`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
        </div>
        
        <div className="flex items-end justify-between mt-4">
          <Typography variant="h2" color="blue-gray" className="font-black">
            {stats.loading ? "..." : value?.toLocaleString()}
          </Typography>
          
          {link && (
            <Link to={link}>
              <Button size="sm" variant="text" color="blue-gray" className="flex items-center gap-2 group hover:bg-gray-300 p-2 normal-case font-bold">
                view report
                <ArrowLongRightIcon className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
          )}
        </div>
      </CardBody>
    </Card>
  );

  return (
    <div className="mt-10 flex w-full flex-col gap-6 min-h-screen pb-10 px-4 bg-slate-50/50">
      
      <Card className="relative w-full overflow-hidden border border-gray-200 bg-gradient-to-br from-white to-gray-500/30 shadow-sm">
        <div className="absolute top-0 right-0 -mt-8 -mr-8 h-48 w-48 rounded-full bg-blue-100/30 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -mb-8 -ml-8 h-48 w-48 rounded-full bg-slate-200/40 blur-3xl"></div>
        
        <CardBody className="flex flex-col items-center justify-center p-12 text-center z-10 relative">
          <div className="mb-4 p-4 bg-white shadow-sm border border-gray-100 rounded-2xl">
            <ServerStackIcon className="h-10 w-10 text-gray-900" />
          </div>
          <Typography variant="h1" color="blue-gray" className="mb-2 font-black tracking-tighter text-6xl">
             <SlotCounter
               value={staticData.totalScrapped + stats.productCount}
               duration={1}
               autoAnimationStart={true}
               startValue={0}
             />
          </Typography>
          <Typography variant="h6" className="font-bold text-gray-400 uppercase tracking-[0.2em] text-xs">
            total aggregated data
          </Typography>
        </CardBody>
      </Card>

      {/* Charts */}
      <div className="mb-6 grid grid-cols-1 gap-y-12 gap-x-6 md:grid-cols-2 xl:grid-cols-3">
        {statisticsChartsData2.map((props) => (
          <StatisticsChart
            key={props.title}
            {...props}
            footer={
              <Typography
                variant="small"
                className="flex items-center font-normal text-blue-gray-600"
              >
                <ClockIcon strokeWidth={2} className="h-4 w-4 text-blue-gray-400" />
                &nbsp;{props.footer}
              </Typography>
            }
          />
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DashboardCard
          title="Product Data"
          subValue="global historical records"
          value={staticData.totalScrapped}
          icon={GlobeAmericasIcon}
          color="from-gray-400 to-gray-600"
          link="/dashboard/productdata-report"
        />

        <DashboardCard
          title="Listing Data"
          subValue="live google maps api"
          value={stats.productCount}
          icon={ArchiveBoxIcon}
          color="from-gray-400 to-gray-600"
          link="/dashboard/listingdata-report"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DashboardCard
          title="Cities Scrapped"
          value={stats.cityCount}
          icon={MapPinIcon}
          color="from-gray-400 to-gray-600"
          link="/dashboard/cities-report"
        />
        <DashboardCard
          title="Categories Scrapped"
          value={stats.categoryCount}
          icon={TagIcon}
          color="from-gray-400 to-gray-600"
          link="/dashboard/categories-report"
        />
        
        {/* --- UPDATED LINKS BELOW --- */}
        <DashboardCard
          title="Cities Pending"
          value={stats.cityCount} // You might want to calculate a pending count specifically later
          icon={ClockIcon}
          color="from-gray-400 to-gray-600"
          link="/dashboard/cities-pending-report" 
        />
        <DashboardCard
          title="Categories Pending"
          value={stats.categoryCount} // You might want to calculate a pending count specifically later
          icon={ClockIcon}
          color="from-gray-400 to-gray-600"
          link="/dashboard/categories-pending-report"
        />
        {/* --------------------------- */}
        
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border border-gray-200 bg-gradient-to-br from-white to-gray-500/30">
          <CardBody className="flex items-center justify-between p-6">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-gray-100 rounded-lg">
                <ChartBarIcon className="h-5 w-5 text-green-600" />
              </div>
              <Typography className="font-bold text-gray-700">total categories</Typography>
            </div>
            <Typography variant="h4" color="blue-gray" className="font-black">
              {stats.categoryCount}
            </Typography>
          </CardBody>
        </Card>

        <Card className="border border-gray-200 bg-gradient-to-br from-white to-gray-500/30">
          <CardBody className="flex items-center justify-between p-6">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-gray-100 rounded-lg">
                <ChartBarIcon className="h-5 w-5 text-green-600" />
              </div>
              <Typography className="font-bold text-gray-700">total areas</Typography>
            </div>
            <Typography variant="h4" color="blue-gray" className="font-black">
              {stats.cityCount}
            </Typography>
          </CardBody>
        </Card>
      </div>

      <footer className="mt-auto pt-8 border-t border-gray-200 text-center md:text-left">
        <Typography variant="small" className="font-medium text-gray-400">
          &copy; {new Date().getFullYear()} scrapemaster dashboard. all rights reserved.
        </Typography>
      </footer>
    </div>
  );
}

export default ReportDashboard;