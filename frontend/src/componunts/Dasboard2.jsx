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
} from "@heroicons/react/24/solid";
import api from "../utils/Api";

export function Dasboard2() {
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
        console.error("Error fetching products:", error);
        setStats((prev) => ({ ...prev, loading: false }));
      }
    };

    fetchProductsData();
  }, []);

  const DashboardCard = ({ title, value, icon: Icon, color, link, subValue }) => (
    <Card className="relative overflow-hidden border border-white/10 bg-gradient-to-br from-gray-900 to-gray-800 shadow-xl transition-transform hover:scale-[1.02] duration-300">
      <CardBody className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <Typography variant="h5" color="white" className="mb-1 font-semibold tracking-wide">
              {title}
            </Typography>
            <Typography className="font-normal text-gray-400 text-sm">
              {subValue || "Updated recently"}
            </Typography>
          </div>
          <div className={`flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${color} shadow-lg ring-1 ring-white/10`}>
            <Icon className="h-6 w-6 text-white" />
          </div>
        </div>
        
        <div className="flex items-end justify-between mt-4">
          <Typography variant="h2" color="white" className="font-bold">
            {stats.loading ? "..." : value?.toLocaleString()}
          </Typography>
          
          {link && (
            <Link to={link}>
              <Button size="sm" variant="text" color="white" className="flex items-center gap-2 group hover:bg-white/10 p-2">
                View More
                <ArrowLongRightIcon className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
          )}
        </div>
      </CardBody>
    </Card>
  );

  return (
    <div className="mt-10 flex w-full flex-col gap-6 min-h-screen pb-10">
      
      <Card className="relative w-full overflow-hidden border border-white/10 bg-gradient-to-r from-gray-600 to-gray-900 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-4 -mr-4 h-32 w-32 rounded-full bg-blue-500/20 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-32 w-32 rounded-full bg-purple-500/20 blur-3xl"></div>
        
        <CardBody className="flex flex-col items-center justify-center p-10 text-center z-10 relative">
          <div className="mb-4 p-3 bg-white/5 rounded-full ring-1 ring-white/10">
            <ServerStackIcon className="h-10 w-10 text-blue-400" />
          </div>
          <Typography variant="h1" color="white" className="mb-2 font-black tracking-tight">
             {(staticData.totalScrapped + stats.productCount).toLocaleString()}
          </Typography>
          <Typography variant="h5" className="font-medium text-blue-gray-200 uppercase tracking-widest opacity-80">
            Total Data Count
          </Typography>
        </CardBody>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DashboardCard
          title="Cities Scrapped"
          value={stats.cityCount}
          icon={MapPinIcon}
          color="from-purple-500 to-indigo-600"
          link="/dashboard/cities-report"
        />
        <DashboardCard
          title="Categories Scrapped"
          value={stats.categoryCount}
          icon={TagIcon}
          color="from-pink-500 to-rose-600"
          link="/dashboard/categories-report"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <DashboardCard
          title="Product Data"
          subValue="Global Historical Records"
          value={staticData.totalScrapped}
          icon={GlobeAmericasIcon}
          color="from-blue-500 to-blue-600"
          link="/dashboard/productdata-report"
        />

        <DashboardCard
          title="Listing Data"
          subValue="Live Google Maps API"
          value={stats.productCount}
          icon={ArchiveBoxIcon}
          color="from-emerald-400 to-emerald-600"
          link="/dashboard/listingdata-report"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border border-white/5 bg-gradient-to-r from-gray-600 to-gray-900">
          <CardBody className="flex items-center justify-between p-4">
            <div className="flex items-center gap-3">
              <ChartBarIcon className="h-5 w-5 text-green-500" />
              <Typography className="font-medium text-white">Total Category Scrapped</Typography>
            </div>
            <Typography variant="h4" color="white" className="font-bold">
              {stats.categoryCount}
            </Typography>
          </CardBody>
        </Card>

        <Card className="border border-white/5 bg-gradient-to-r from-gray-600 to-gray-900">
          <CardBody className="flex items-center justify-between p-4">
            <div className="flex items-center gap-3">
              <ChartBarIcon className="h-5 w-5 text-green-500" />
              <Typography className="font-medium text-white">Total Area Scrapped</Typography>
            </div>
            <Typography variant="h4" color="white" className="font-bold">
              {stats.cityCount}
            </Typography>
          </CardBody>
        </Card>
      </div>

      <footer className="mt-auto pt-6 border-t border-white/10 text-center md:text-left">
        <Typography variant="small" className="font-normal text-white/40">
          &copy; {new Date().getFullYear()} ScrapeMaster Dashboard. All Rights Reserved.
        </Typography>
      </footer>
    </div>
  );
}

export default Dasboard2;