import React, { useEffect, useState, useCallback } from "react";
import api from "@/utils/Api"; // Assuming this instance handles your base URL
import { Card, CardBody, CardHeader, Typography, Input, Spinner, Button } from "@material-tailwind/react";
import { ChevronLeftIcon, ChevronRightIcon, ArrowDownTrayIcon, MapPinIcon, ChartBarIcon } from "@heroicons/react/24/solid";

const locColumns = [
  { key: "area", label: "Area Name" },
  { key: "city", label: "City" },
  { key: "state", label: "State (Code)" },
  { key: "total_records", label: "Business Density" },
];

const LocationMasterData = () => {
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({ area: "", city: "", state: "" });

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      // NO /api HERE. Calling the route exactly as registered in app.py
      const res = await api.get("/location-master/fetch-data", {
        params: { page: currentPage, ...filters }
      });
      if (res.data.status === "SUCCESS") {
        setPageData(res.data.data || []);
        setTotalPages(res.data.total_pages || 1);
      }
    } catch (err) { console.error("Location Master Fetch Error:", err); }
    finally { setLoading(false); }
  }, [currentPage, filters]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <StatCard title="Total Areas" value={pageData.length} icon={<MapPinIcon className="h-6 w-6 text-blue-500" />} />
        <StatCard title="Top Density" value={pageData[0]?.area || "N/A"} icon={<ChartBarIcon className="h-6 w-6 text-green-500" />} />
      </div>

      <Card className="shadow-lg border border-gray-200">
        <CardHeader floated={false} shadow={false} className="p-4">
          <div className="flex justify-between items-center mb-4">
            <Typography variant="h5" color="blue-gray">India Location Registry</Typography>
            <Button size="sm" color="indigo" className="flex items-center gap-2">
               <ArrowDownTrayIcon className="h-4 w-4" /> Export XLSX
            </Button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t pt-4">
            <Input label="Search Area" onChange={(e) => setFilters({...filters, area: e.target.value})} />
            <Input label="Filter City" onChange={(e) => setFilters({...filters, city: e.target.value})} />
            <Input label="Filter State" onChange={(e) => setFilters({...filters, state: e.target.value})} />
          </div>
        </CardHeader>
        <CardBody className="overflow-auto px-0 py-0">
          {loading ? <div className="flex justify-center p-10"><Spinner /></div> : (
            <table className="w-full text-left table-auto">
              <thead>
                <tr className="bg-gray-50 border-b">
                  {locColumns.map(col => <th key={col.key} className="p-4 font-bold text-xs uppercase text-gray-600">{col.label}</th>)}
                </tr>
              </thead>
              <tbody>
                {pageData.map((row) => (
                  <tr key={row.id} className="hover:bg-gray-50 border-b transition-colors">
                    <td className="p-4 text-sm font-bold text-blue-gray-800">{row.area}</td>
                    <td className="p-4 text-sm"><span className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs font-black">{row.city}</span></td>
                    <td className="p-4 text-sm text-gray-600">{row.state}</td>
                    <td className="p-4 text-sm font-black text-indigo-600">
                      {row.total_records?.toLocaleString()} <span className="text-[10px] text-gray-400 font-normal ml-1">RECORDS</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </CardBody>
        <div className="p-4 border-t flex items-center justify-between">
          <Typography variant="small">Page {currentPage} of {totalPages}</Typography>
          <div className="flex gap-2">
            <Button variant="outlined" size="sm" disabled={currentPage === 1} onClick={() => setCurrentPage(p => p - 1)}>Prev</Button>
            <Button variant="outlined" size="sm" disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p + 1)}>Next</Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

const StatCard = ({ title, value, icon }) => (
    <Card className="p-4 border shadow-sm flex flex-row items-center gap-4">
        <div className="p-3 bg-gray-50 rounded-lg">{icon}</div>
        <div>
            <Typography variant="small" className="font-bold text-gray-400 uppercase">{title}</Typography>
            <Typography variant="h5" color="blue-gray" className="font-black">{value}</Typography>
        </div>
    </Card>
);

export default LocationMasterData;