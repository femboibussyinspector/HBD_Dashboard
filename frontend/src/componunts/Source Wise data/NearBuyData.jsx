import React, { useEffect, useState, useCallback } from "react";
import { Card, CardBody, CardHeader, Typography, Input, Spinner, Button } from "@material-tailwind/react";
import { ChevronLeftIcon, ChevronRightIcon, ArrowDownTrayIcon } from "@heroicons/react/24/solid";
import * as XLSX from "xlsx";
import api from "@/utils/Api";

const nbColumns = [
  { key: "name", label: "Business Name", width: "w-3/12" },
  { key: "address", label: "Address", width: "w-3/12" },
  { key: "number", label: "Contact", width: "w-2/12" },
  { key: "city", label: "City", width: "w-1/12" },
  { key: "rating", label: "Rating", width: "w-1/12" },
];

const NearBuyData = () => {
  const [loading, setLoading] = useState(true);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get("/nearbuy/fetch-data", {
        params: { page: currentPage, limit: 10, search }
      });
      setPageData(res.data.data || []);
      setTotalPages(res.data.total_pages || 1);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  }, [currentPage, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="p-6">
      <Card>
        <CardHeader floated={false} shadow={false} className="p-4">
          <Typography variant="h5">Near Buy Data Master</Typography>
          <div className="w-72 mt-4">
            <Input label="Search Business" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
        </CardHeader>
        <CardBody className="overflow-scroll px-0 py-0">
          {loading ? <Spinner className="mx-auto my-10" /> : (
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50">
                  {nbColumns.map(col => <th key={col.key} className="p-4 border-b font-bold">{col.label}</th>)}
                </tr>
              </thead>
              <tbody>
                {pageData.map((row, i) => (
                  <tr key={i} className="hover:bg-gray-50 border-b">
                    {nbColumns.map(col => <td key={col.key} className="p-4">{row[col.key] || "-"}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>
    </div>
  );
};

export default NearBuyData;