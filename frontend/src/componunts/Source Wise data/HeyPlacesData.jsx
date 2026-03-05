import React, { useEffect, useState, useCallback } from "react";
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
import api from "@/utils/Api"; // Importing your configured Axios instance

// 1. Updated Columns to perfectly match your DB screenshot
const heyPlacesColumns = [
  { key: "name", label: "Business Name", width: 250 },
  { key: "address", label: "Address", width: 350 },
  { key: "number", label: "Contact No", width: 150 },
  { key: "website", label: "Website", width: 200 },
  { key: "category", label: "Category", width: 180 },
  { key: "city", label: "City", width: 150 },
];

const HeyPlacesData = () => {
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [error, setError] = useState(null);
  const limit = 10;

  const [search, setSearch] = useState("");
  const [citySearch, setCitySearch] = useState("");

  // 2. Fixed API Fetching Logic (No more localhost traps)
  const fetchHeyPlacesData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Calling your live backend via the api utility
      const response = await api.get("/heyplaces/fetch-data", {
        params: {
          page: currentPage,
          limit: limit,
          search: search,
          city: citySearch,
        }
      });
      
      // Axios puts the JSON response inside the .data object
      const result = response.data;
      
      setPageData(result.data || []);
      setTotalPages(result.total_pages || 1);
      setTotalRecords(result.total_count || 0);
    } catch (err) {
      console.error("Fetch Error:", err);
      if (err.response && err.response.status === 401) {
        setError("Session expired. Please log in again.");
      } else {
        setError("Failed to fetch HeyPlaces data from backend.");
      }
    } finally {
      setLoading(false);
    }
  }, [currentPage, search, citySearch]);

  useEffect(() => {
    fetchHeyPlacesData();
  }, [fetchHeyPlacesData]);

  // Reset to page 1 if the user starts typing in search boxes
  useEffect(() => {
    setCurrentPage(1);
  }, [search, citySearch]);

  const exportToExcel = () => {
    if (!pageData.length) return;
    const ws = XLSX.utils.json_to_sheet(pageData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "HeyPlaces_Data");
    XLSX.writeFile(wb, `HeyPlaces_Page_${currentPage}.xlsx`);
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 rounded bg-white text-black">
      <div className="flex justify-between items-end mb-6">
        <div>
          <Typography variant="h4" className="font-bold text-blue-gray-900">
            HeyPlaces Listing Master
          </Typography>
          <Typography variant="small" className="font-medium text-gray-500">
            {error ? (
              <span className="text-red-500 font-bold">{error}</span>
            ) : (
              `Displaying verified records from HeyPlaces (${totalRecords} total)`
            )}
          </Typography>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="gradient" 
            color="green" 
            size="sm" 
            className="flex items-center gap-2"
            onClick={exportToExcel}
          >
            <ArrowDownTrayIcon className="h-4 w-4" /> Export Page
          </Button>
          <Button 
            variant="outlined" 
            size="sm" 
            className="flex items-center gap-2"
            onClick={fetchHeyPlacesData}
          >
            <ArrowPathIcon className="h-4 w-4" /> Refresh
          </Button>
        </div>
      </div>

      <Card className="h-full w-full border border-blue-gray-100 shadow-sm">
        <CardHeader floated={false} shadow={false} className="rounded-none p-4 bg-white">
          <div className="flex flex-wrap items-center justify-between gap-y-4">
            <div className="flex w-full shrink-0 gap-2 md:w-max">
              <div className="w-72">
                <Input 
                  label="Search Business Name" 
                  value={search} 
                  onChange={(e) => setSearch(e.target.value)} 
                />
              </div>
              <div className="w-48">
                <Input 
                  label="Filter by City" 
                  value={citySearch} 
                  onChange={(e) => setCitySearch(e.target.value)} 
                />
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <Typography variant="small" className="font-bold text-blue-gray-700">
                Page {currentPage} of {totalPages}
              </Typography>
              <div className="flex gap-2">
                <Button 
                  variant="outlined" 
                  size="sm" 
                  disabled={currentPage === 1 || loading} 
                  onClick={() => setCurrentPage(p => p - 1)}
                >
                  Previous
                </Button>
                <Button 
                  variant="outlined" 
                  size="sm" 
                  disabled={currentPage === totalPages || totalPages === 0 || loading} 
                  onClick={() => setCurrentPage(p => p + 1)}
                >
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
              <Typography className="animate-pulse font-medium text-gray-600">
                Fetching HeyPlaces Data...
              </Typography>
            </div>
          ) : (
            <table className="w-full min-w-[1200px] table-fixed text-left">
              <thead>
                <tr>
                  {heyPlacesColumns.map((col) => (
                    <th
                      key={col.key}
                      style={{ width: col.width }}
                      className="border-y border-blue-gray-100 bg-gray-50/50 p-4 transition-colors"
                    >
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="flex items-center justify-between gap-2 font-bold leading-none opacity-70"
                      >
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
                      {heyPlacesColumns.map((col) => (
                        <td key={col.key} className="p-4 border-b border-blue-gray-50">
                          {col.key === "website" && row[col.key] && row[col.key] !== "-" && row[col.key] !== "N/A" ? (
                            <a 
                              href={row[col.key].startsWith('http') ? row[col.key] : `https://${row[col.key]}`} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-blue-500 hover:underline break-all text-sm font-medium"
                            >
                              {row[col.key]}
                            </a>
                          ) : (
                            <Typography variant="small" color="blue-gray" className="font-normal break-words">
                              {row[col.key] || "-"}
                            </Typography>
                          )}
                        </td>
                      ))}
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={heyPlacesColumns.length} className="p-20 text-center">
                      <Typography variant="h6" color="blue-gray" className="opacity-40 italic">
                        {error || "No records found in HeyPlaces table"}
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

export default HeyPlacesData;