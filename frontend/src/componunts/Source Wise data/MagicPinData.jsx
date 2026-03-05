import React, { useEffect, useState, useCallback } from "react";
import { Card, CardBody, CardHeader, Typography, Input, Spinner, Button } from "@material-tailwind/react";
import { ChevronLeftIcon, ChevronRightIcon, ArrowDownTrayIcon } from "@heroicons/react/24/solid";
import * as XLSX from "xlsx";
import api from "@/utils/Api";

const mpColumns = [
  { key: "name", label: "Business Name", width: "w-3/12" },
  { key: "number", label: "Contact", width: "w-2/12" },
  { key: "rating", label: "Rating", width: "w-1/12" },
  { key: "avg_spent", label: "Avg Spent", width: "w-1/12" },
  { key: "address", label: "Address", width: "w-3/12" },
  { key: "city", label: "City", width: "w-1/12" },
  { key: "category", label: "Category", width: "w-1/12" },
];

const MagicPinData = () => {
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [search, setSearch] = useState("");
  const [citySearch, setCitySearch] = useState("");

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get("/magicpin/fetch-data", {
        params: { page: currentPage, limit: 10, search, city: citySearch }
      });
      setPageData(res.data.data || []);
      setTotalPages(res.data.total_pages || 1);
      setTotalRecords(res.data.total_count || 0);
    } catch (err) {
      console.error("MagicPin Frontend Error:", err);
    } finally {
      setLoading(false);
    }
  }, [currentPage, search, citySearch]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleDownload = () => {
    const worksheet = XLSX.utils.json_to_sheet(pageData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "MagicPin_Data");
    XLSX.writeFile(workbook, "MagicPin_Export.xlsx");
  };

  return (
    <div className="p-6">
      <Card className="h-full w-full">
        <CardHeader floated={false} shadow={false} className="rounded-none p-4">
          <div className="mb-4 flex items-center justify-between gap-8">
            <div>
              <Typography variant="h5" color="blue-gray">Magic Pin Data Master</Typography>
              <Typography color="gray" className="mt-1 font-normal">
                Total Records: {totalRecords}
              </Typography>
            </div>
            <Button size="sm" className="flex items-center gap-2" onClick={handleDownload}>
              <ArrowDownTrayIcon className="h-4 w-4" /> Export XLSX
            </Button>
          </div>
          <div className="flex flex-col justify-between gap-4 md:flex-row">
            <div className="w-full md:w-72">
              <Input label="Search Business Name" value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} />
            </div>
            <div className="w-full md:w-72">
              <Input label="Filter by City" value={citySearch} onChange={(e) => { setCitySearch(e.target.value); setCurrentPage(1); }} />
            </div>
          </div>
        </CardHeader>

        <CardBody className="overflow-scroll px-0 py-0">
          {loading ? (
            <div className="flex justify-center items-center h-64"><Spinner className="h-10 w-10" /></div>
          ) : (
            <table className="w-full min-w-max table-auto text-left">
              <thead>
                <tr>
                  {mpColumns.map((col) => (
                    <th key={col.key} className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4">
                      <Typography variant="small" color="blue-gray" className="font-bold leading-none opacity-70">
                        {col.label}
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pageData.length > 0 ? pageData.map((row, index) => (
                  <tr key={index} className="even:bg-blue-gray-50/50">
                    {mpColumns.map((col) => (
                      <td key={col.key} className="p-4 border-b border-blue-gray-50">
                        <Typography variant="small" color="blue-gray" className="font-normal">
                          {row[col.key] || "-"}
                        </Typography>
                      </td>
                    ))}
                  </tr>
                )) : (
                  <tr>
                    <td colSpan={mpColumns.length} className="p-4 text-center">No records found.</td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </CardBody>

        <div className="flex items-center justify-between border-t border-blue-gray-50 p-4">
          <Typography variant="small" color="blue-gray" className="font-normal">
            Page {currentPage} of {totalPages}
          </Typography>
          <div className="flex gap-2">
            <Button variant="outlined" size="sm" disabled={currentPage === 1} onClick={() => setCurrentPage(prev => prev - 1)}>
              <ChevronLeftIcon className="h-4 w-4 mr-1" /> Previous
            </Button>
            <Button variant="outlined" size="sm" disabled={currentPage === totalPages} onClick={() => setCurrentPage(prev => prev + 1)}>
              Next <ChevronRightIcon className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default MagicPinData;