import React, { useEffect, useState, useCallback } from "react";
import api from "@/utils/Api";
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Spinner,
} from "@material-tailwind/react";
import {
  ChevronUpDownIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon
} from "@heroicons/react/24/solid";
import * as XLSX from "xlsx/dist/xlsx.full.min.js";

const gmsColumns = [
  { key: "name", label: "Business Name", width: "w-3/12" },
  { key: "category", label: "Category", width: "w-2/12" },
  { key: "address", label: "Address", width: "w-4/12" },
  { key: "number", label: "Contact No", width: "w-1/12" },
  { key: "rating", label: "Rating", width: "w-1/12" },
  { key: "review_count", label: "Reviews", width: "w-1/12" },
];

const GoogleMapData = () => {
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [error, setError] = useState(null);
  const limit = 10;

  const [search, setSearch] = useState("");
  const [citySearch, setCitySearch] = useState("");

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get("/google-map-scrape/fetch-data", {
        params: { page: currentPage, limit, search, city: citySearch }
      });
      
      const result = response.data;
      setPageData(result.data || []);
      setTotalPages(result.total_pages || 1);
      setTotalRecords(result.total_count || 0);
    } catch (err) {
      console.error("Fetch Error:", err);
      setError("Failed to fetch Google Map Scrape data.");
    } finally {
      setLoading(false);
    }
  }, [currentPage, search, citySearch]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const exportToExcel = () => {
    if (!pageData.length) return;
    const ws = XLSX.utils.json_to_sheet(pageData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "GoogleMapScrape_Data");
    XLSX.writeFile(wb, `GoogleMapScrape_Page_${currentPage}.xlsx`);
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 rounded bg-white text-black">
      <div className="flex justify-between items-end mb-6">
        <div>
          <Typography variant="h4" className="font-bold text-blue-gray-900">
            Google Map Scrape Master
          </Typography>
          <Typography variant="small" className="font-medium text-gray-500">
            {error ? (
              <span className="text-red-500 font-bold">{error}</span>
            ) : (
              `Displaying scraped records (${totalRecords} total)`
            )}
          </Typography>
        </div>
        <div className="flex gap-2">
          <Button variant="gradient" color="green" size="sm" className="flex items-center gap-2" onClick={exportToExcel}>
            <ArrowDownTrayIcon className="h-4 w-4" /> Export Page
          </Button>
          <Button variant="outlined" size="sm" className="flex items-center gap-2" onClick={fetchData}>
            <ArrowPathIcon className="h-4 w-4" /> Refresh
          </Button>
        </div>
      </div>

      <Card className="h-full w-full border border-blue-gray-100">
        <CardHeader floated={false} shadow={false} className="rounded-none p-4 bg-blue-gray-50/50">
          <div className="flex flex-wrap items-center justify-between gap-y-4">
            <div className="flex w-full shrink-0 gap-2 md:w-max">
              <div className="w-72">
                <Input label="Search Business Name" value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} />
              </div>
              <div className="w-48">
                <Input label="Filter by City/Address" value={citySearch} onChange={(e) => { setCitySearch(e.target.value); setCurrentPage(1); }} />
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <Typography variant="small" className="font-bold text-blue-gray-700">
                Page {currentPage} of {totalPages}
              </Typography>
              <div className="flex gap-2">
                <Button variant="outlined" size="sm" disabled={currentPage === 1 || loading} onClick={() => setCurrentPage(p => p - 1)}>
                  Previous
                </Button>
                <Button variant="outlined" size="sm" disabled={currentPage === totalPages || loading} onClick={() => setCurrentPage(p => p + 1)}>
                  Next
                </Button>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardBody className="overflow-x-auto p-0">
          {loading ? (
            <div className="flex flex-col justify-center py-24 items-center gap-4">
              <Spinner className="h-10 w-10 text-blue-500" />
            </div>
          ) : (
            <table className="w-full min-w-max table-auto text-left">
              <thead>
                <tr>
                  {gmsColumns.map((col) => (
                    <th key={col.key} className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4 transition-colors">
                      <Typography variant="small" color="blue-gray" className="flex items-center justify-between gap-2 font-bold leading-none opacity-70">
                        {col.label} <ChevronUpDownIcon strokeWidth={2} className="h-4 w-4" />
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pageData.length > 0 ? (
                  pageData.map((row, index) => (
                    <tr key={index} className="even:bg-blue-gray-50/50 hover:bg-blue-50 transition-colors">
                      {gmsColumns.map((col) => (
                        <td key={col.key} className="p-4 border-b border-blue-gray-50">
                          <Typography variant="small" color="blue-gray" className="font-normal break-words">
                            {row[col.key] || "-"}
                          </Typography>
                        </td>
                      ))}
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={gmsColumns.length} className="p-20 text-center">
                      <Typography variant="h6" color="blue-gray" className="opacity-40 italic">
                        {error || "No records found"}
                      </Typography>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>
    </div>
  );
};

export default GoogleMapData;