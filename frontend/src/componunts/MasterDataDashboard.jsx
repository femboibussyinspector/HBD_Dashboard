import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { 
  ServerStackIcon, 
  StarIcon, 
  MapIcon, 
  TagIcon, 
  ChartBarIcon, 
  PhoneIcon 
} from "@heroicons/react/24/solid";
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, Legend 
} from "recharts";

const MasterDataDashboard = () => {
  const [searchParams] = useSearchParams();
  const taskId = searchParams.get("task_id");
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const query = taskId ? `?task_id=${taskId}` : "";
        const response = await fetch(`https://dashboard.cityhangaround.com/api/master-dashboard-stats${query}`, {
          headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        });
        const result = await response.json();
        if (result.status === "COMPLETED") setDashboardData(result.stats);
      } catch (err) { console.error("Fetch error:", err); }
    };
    fetchData();
  }, [taskId]);

  if (!dashboardData) return (
    <div className="flex h-screen items-center justify-center bg-gray-50 flex-col">
      <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mb-6"></div>
      <h2 className="text-2xl font-bold text-gray-700">Loading Registry Data...</h2>
    </div>
  );

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* 1. KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-blue-500">
           <p className="text-gray-500 font-bold text-sm uppercase">Total Master Records</p>
           <h1 className="text-4xl font-black text-gray-800">{dashboardData.total_records.toLocaleString()}</h1>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-teal-500">
           <p className="text-gray-500 font-bold text-sm uppercase">Average Rating</p>
           <h1 className="text-4xl font-black text-gray-800">{dashboardData.avg_system_rating} ★</h1>
        </div>
      </div>

      {/* 2. Top Section: State Table & Phone Chart */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <SummaryTable 
            title="State Distribution" 
            data={dashboardData.state_summary} 
            label="State" 
        />
        
        {/* FIXED: Replaced SummaryTable with ChartBox for Phone Distribution */}
        <ChartBox title="Phone Number Availability" icon={<PhoneIcon className="w-5 h-5 text-green-500"/>}>
          <PieChart>
            <Pie 
              data={dashboardData.phone_distribution || []} 
              innerRadius={60} 
              outerRadius={80} 
              paddingAngle={5}
              dataKey="value" 
              nameKey="name"
            >
              {(dashboardData.phone_distribution || []).map((entry, i) => (
                <Cell key={`cell-${i}`} fill={entry.fill} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => value.toLocaleString()} />
            <Legend verticalAlign="bottom" />
          </PieChart>
        </ChartBox>
      </div>

      {/* 3. Bar Charts: Cities & Subcategories */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <ChartBox title="Top 10 Cities" icon={<MapIcon className="w-5 h-5 text-red-400"/>}>
          <BarChart data={dashboardData.top_cities} layout="vertical" barCategoryGap="20%">
            <XAxis type="number" hide />
            <YAxis dataKey="name" type="category" width={100} tick={{fontSize: 11}} axisLine={false} tickLine={false} />
            <Tooltip cursor={{fill: 'transparent'}} />
            <Bar dataKey="count" fill="#f87171" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ChartBox>

        <ChartBox title="Top Subcategories" icon={<TagIcon className="w-5 h-5 text-indigo-400"/>}>
          <BarChart data={dashboardData.top_subcategories} layout="vertical" barCategoryGap="20%">
            <XAxis type="number" hide />
            <YAxis dataKey="name" type="category" width={150} tick={{fontSize: 10}} axisLine={false} tickLine={false} />
            <Tooltip cursor={{fill: 'transparent'}} />
            <Bar dataKey="count" fill="#6366f1" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ChartBox>
      </div>

      {/* 4. Top Rated Businesses Table */}
      <div className="bg-white rounded-xl shadow-sm p-6 border transition hover:shadow-md">
        <h3 className="text-lg font-bold text-gray-700 mb-4 flex items-center gap-2">
          <ChartBarIcon className="w-5 h-5 text-indigo-500" /> Top Rated Businesses
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-xs text-gray-500 uppercase">
              <tr>
                <th className="p-3">Name</th>
                <th className="p-3">Listings Count</th>
                <th className="p-3">City</th>
                <th className="p-3">Rating</th>
              </tr>
            </thead>
            <tbody>
              {dashboardData.top_rated_businesses.map(biz => (
                <tr key={biz.id} className="border-b hover:bg-gray-50">
                  <td className="p-3 font-bold text-gray-800">{biz.name}</td>
                  <td className="p-3 text-sm">
                    <span className="bg-indigo-100 text-indigo-700 px-2 py-1 rounded font-bold">
                        {biz.count}
                    </span>
                  </td>
                  <td className="p-3 text-gray-600">{biz.city}</td>
                  <td className="p-3 text-amber-500 font-bold">{biz.stars} ★</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const SummaryTable = ({ title, data, label }) => (
  <div className="bg-white p-6 rounded-xl border shadow-sm h-96 overflow-hidden flex flex-col">
    <h3 className="font-bold text-gray-700 mb-4">{title}</h3>
    <div className="flex-1 overflow-y-auto">
        <table className="w-full text-sm">
          <thead className="text-gray-400 border-b sticky top-0 bg-white">
            <tr><th className="text-left pb-2">{label}</th><th className="text-right pb-2">Count</th></tr>
          </thead>
          <tbody>
            {(data || []).map((item, i) => (
              <tr key={i} className="border-b last:border-none">
                <td className="py-3 font-medium text-gray-700">{item.state || item.data_source}</td>
                <td className="py-3 text-right font-bold text-blue-600">{item.count?.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
    </div>
  </div>
);

const ChartBox = ({ title, icon, children }) => (
  <div className="bg-white rounded-xl shadow-sm p-6 border h-96 flex flex-col transition hover:shadow-md">
    <div className="flex justify-between items-center mb-4">
      <h3 className="font-bold text-gray-700">{title}</h3>
      {icon}
    </div>
    <div className="flex-1 min-h-[250px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        {children}
      </ResponsiveContainer>
    </div>
  </div>
);

export default MasterDataDashboard;