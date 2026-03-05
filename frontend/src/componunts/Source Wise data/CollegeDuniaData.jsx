import React, { useEffect, useState, useCallback } from "react";
import api from "@/utils/Api"; // Use your existing axios utility
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

// Updated keys to match the database image fields
const collegeDuniaColumns = [
  { key: "name", label: "Institution Name", width: 220 },
  { key: "address", label: "Address", width: 320 },
  { key: "number", label: "Contact No", width: 140 }, // Changed from phone_number
  { key: "category", label: "Category", width: 160 },
  { key: "city", label: "City", width: 120 },
  { key: "area", label: "Area", width: 140 },
  { key: "avg_fees", label: "Avg Fees", width: 120 }, // Added from image fields
];

const CollegeDuniaData = () => { // Renamed for consistency
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [error, setError] = useState(null);
  const limit = 10;

  const [search, setSearch] = useState("");
  const [citySearch, setCitySearch] = useState("");

  const fetchCollegeDuniaData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const queryParams = new URLSearchParams({
        page: currentPage,
        limit: limit,
        search: search,
        city: citySearch,
      });

      // Point to the correct Flask endpoint on port 8000
      const response = await api.get(`/college-dunia/fetch-data?${queryParams}`);
      const result = response.data;
      
      setPageData(result.data || []);
      setTotalPages(result.total_pages || 1);
      setTotalRecords(result.total_count || 0);
    } catch (err) {
      console.error("Fetch Error:", err);
      if (err.code === "ERR_NETWORK") {
        setError("Backend offline. Ensure Flask port 8000 is running.");
      } else {
        setError("Failed to fetch College Dunia data.");
      }
    } finally {
      setLoading(false);
    }
  }, [currentPage, search, citySearch]);

  useEffect(() => {
    fetchCollegeDuniaData();
  }, [fetchCollegeDuniaData]);

  const exportToExcel = () => {
    if (!pageData.length) return;
    const ws = XLSX.utils.json_to_sheet(pageData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "CollegeDunia_Data");
    XLSX.writeFile(wb, `CollegeDunia_Page_${currentPage}.xlsx`);
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 rounded bg-white text-black">
      <div className="flex justify-between items-end mb-6">
        <div>
          <Typography variant="h4" className="font-bold text-blue-gray-900">
            College Dunia Data Master
          </Typography>
          <Typography variant="small" className="font-medium text-gray-500">
            {error ? (
              <span className="text-red-500 font-bold">{error}</span>
            ) : (
              `Records: ${totalRecords} total`
            )}
          </Typography>
        </div>
        <div className="flex gap-2">
          <Button variant="gradient" color="green" size="sm" className="flex items-center gap-2" onClick={exportToExcel}>
            <ArrowDownTrayIcon className="h-4 w-4" /> Export
          </Button>
          <Button variant="outlined" size="sm" className="flex items-center gap-2" onClick={fetchCollegeDuniaData}>
            <ArrowPathIcon className="h-4 w-4" /> Refresh
          </Button>
        </div>
      </div>

      <Card className="h-full w-full border border-blue-gray-100">
        <CardHeader floated={false} shadow={false} className="rounded-none p-4 bg-blue-gray-50/50">
          <div className="flex flex-wrap items-center justify-between gap-y-4">
            <div className="flex w-full shrink-0 gap-2 md:w-max">
              <div className="w-72">
                <Input label="Search Institution" value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} />
              </div>
              <div className="w-48">
                <Input label="Filter City" value={citySearch} onChange={(e) => { setCitySearch(e.target.value); setCurrentPage(1); }} />
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <Typography variant="small" className="font-bold text-blue-gray-700">
                Page {currentPage} of {totalPages}
              </Typography>
              <div className="flex gap-2">
                <Button variant="outlined" size="sm" disabled={currentPage === 1 || loading} onClick={() => setCurrentPage(p => p - 1)}>Prev</Button>
                <Button variant="outlined" size="sm" disabled={currentPage === totalPages || loading} onClick={() => setCurrentPage(p => p + 1)}>Next</Button>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardBody className="overflow-x-auto p-0">
          {loading ? (
            <div className="flex flex-col justify-center py-24 items-center gap-4">
              <Spinner className="h-10 w-10 text-blue-500" />
              <Typography className="animate-pulse">Fetching College Data...</Typography>
            </div>
          ) : (
            <table className="w-full min-w-[1200px] table-fixed text-left">
              <thead>
                <tr>
                  {collegeDuniaColumns.map((col) => (
                    <th key={col.key} style={{ width: col.width }} className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4">
                      <Typography variant="small" color="blue-gray" className="font-bold opacity-70">{col.label}</Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pageData.length > 0 ? (
                  pageData.map((row, idx) => (
                    <tr key={idx} className="even:bg-blue-gray-50/50 hover:bg-blue-50 transition-colors">
                      {collegeDuniaColumns.map((col) => (
                        <td key={col.key} className="p-4 border-b border-blue-gray-50">
                          <Typography variant="small" className="font-normal break-words">{row[col.key] || "-"}</Typography>
                        </td>
                      ))}
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={collegeDuniaColumns.length} className="p-20 text-center italic opacity-40">
                      {error || "No college records found."}
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

export default CollegeDuniaData;