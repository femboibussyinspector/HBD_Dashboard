import React, { useEffect, useMemo, useState } from "react";
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
  MagnifyingGlassIcon,
  ChevronUpDownIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/solid";

import { listingData } from "@/data/listingJSON";
import * as XLSX from "xlsx/dist/xlsx.full.min.js";

const defaultColumns = [
  { key: "name", label: "Name", width: 220 },
  { key: "address", label: "Address", width: 320 },
  { key: "website", label: "Website", width: 180 },
  { key: "phone_number", label: "Contact", width: 140 },
  { key: "reviews_count", label: "Review Count", width: 120 },
  { key: "reviews_average", label: "Review Avg", width: 120 },
  { key: "category", label: "Category", width: 140 },
  { key: "subcategory", label: "Sub-Category", width: 140 },
  { key: "source", label: "Source", width: 120 }, // ✅ NEW
  { key: "city", label: "City", width: 140 },
  { key: "state", label: "State", width: 140 },
  { key: "area", label: "Area", width: 140 },
];

// CSV Converter
const convertToCSV = (arr) => {
  if (!arr?.length) return "";
  const headers = Object.keys(arr[0]);
  const rows = arr.map((r) =>
    headers.map((h) => `"${String(r[h] ?? "").replace(/"/g, "'")}"`).join(",")
  );
  return [headers.join(","), ...rows].join("\n");
};

const CleanListingMaster = () => {
  const [loading, setLoading] = useState(true);
  const [fullData, setFullData] = useState([]);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 20;

  const [search, setSearch] = useState("");
  const [areaSearch, setAreaSearch] = useState("");
  const [sourceFilter, setSourceFilter] = useState(""); // ✅ NEW

  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  const [columns] = useState(defaultColumns);

  // Load Data
  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setFullData(listingData);
      setTotal(listingData.length);
      setLoading(false);
    }, 300);
  }, []);

  // Reset page on filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [search, areaSearch, sourceFilter]);

  // Filter Data
  const filteredData = useMemo(() => {
    let data = [...fullData];
    const safe = (v) => String(v ?? "").toLowerCase();

    if (search) {
      const s = search.toLowerCase();
      data = data.filter((x) => safe(x.name).includes(s));
    }

    if (areaSearch) {
      const s = areaSearch.toLowerCase();
      data = data.filter((x) => safe(x.category).includes(s));
    }

    if (sourceFilter) {
      data = data.filter(
        (x) => safe(x.source) === sourceFilter.toLowerCase()
      );
    }

    return data;
  }, [fullData, search, areaSearch, sourceFilter]);

  // Source Counts
  const sourceCounts = useMemo(() => {
    const counts = {};
    filteredData.forEach((x) => {
      const s = x.source || "unknown";
      counts[s] = (counts[s] || 0) + 1;
    });
    return counts;
  }, [filteredData]);

  // Sort
  const sortedData = useMemo(() => {
    if (!sortField) return filteredData;

    return [...filteredData].sort((a, b) => {
      const A = String(a[sortField] ?? "").toLowerCase();
      const B = String(b[sortField] ?? "").toLowerCase();
      if (A === B) return 0;
      return sortOrder === "asc" ? (A > B ? 1 : -1) : (A < B ? 1 : -1);
    });
  }, [filteredData, sortField, sortOrder]);

  // Pagination
  useEffect(() => {
    const start = (currentPage - 1) * limit;
    setPageData(sortedData.slice(start, start + limit));
    setTotal(sortedData.length);
  }, [sortedData, currentPage]);

  const totalPages = Math.max(1, Math.ceil(total / limit));

  const toggleSort = (field) => {
    if (sortField === field) {
      setSortOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  // CSV
  const downloadCSV = (currentOnly = false) => {
    const arr = currentOnly ? pageData : sortedData;
    const csv = convertToCSV(arr);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = currentOnly ? "listing_page.csv" : "listing_all.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  // Excel
  const downloadExcel = (currentOnly = false) => {
    const arr = currentOnly ? pageData : sortedData;
    if (!arr.length) return;

    const ws = XLSX.utils.json_to_sheet(arr);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Listings");
    XLSX.writeFile(wb, currentOnly ? "listing_page.xlsx" : "listing_all.xlsx");
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 rounded bg-white text-black">
      <div className="flex justify-between items-center mb-4">
        <Typography variant="h4" className="pb-2">Clean Listing Data</Typography>

        <div className="flex gap-2">
          <Button size="sm" onClick={() => downloadCSV(false)}>CSV All</Button>
          <Button size="sm" onClick={() => downloadCSV(true)}>CSV Page</Button>
          <Button size="sm" onClick={() => downloadExcel(false)}>Excel All</Button>
          <Button size="sm" onClick={() => downloadExcel(true)}>Excel Page</Button>
        </div>
      </div>

      {/* Source Badges */}
      {/* <div className="flex gap-3 mb-3 text-sm">
        {Object.entries(sourceCounts).map(([k, v]) => (
          <span key={k} className="px-3 py-1 border rounded bg-gray-100">
            {k} : {v}
          </span>
        ))}
      </div> */}

      <Card className="border">
        <CardHeader className="flex flex-wrap justify-between gap-3 p-4 bg-gray-100">
          <div className="flex gap-3 flex-wrap">
            <Input label="Search Name..." value={search} onChange={(e) => setSearch(e.target.value)} />
            <Input label="Search Category..." value={areaSearch} onChange={(e) => setAreaSearch(e.target.value)} />
            <select
              value={sourceFilter}
              onChange={(e) => setSourceFilter(e.target.value)}
              className="border rounded px-3 py-2 bg-gray-100 text-sm"
            >
              <option value="">All Sources</option>
              <option value="asklaila">Asklaila</option>
              <option value="atm">ATM</option>
              <option value="bank">Bank</option>
              <option value="college-dunia">CollegeDunia</option>
              <option value="google">Google</option>
              <option value="google-maps">Google Maps</option>
              <option value="hey-places">HeyPlaces</option>
              <option value="just-dial">JustDial</option>
              <option value="magicpin">MagicPin</option>
              <option value="nearbuy">Near Buy</option>
              <option value="pinda">Pinda</option>
              <option value="post-office-india">Post Office India</option>
              <option value="schoolgis">Schoolgis</option>
              <option value="shiksha">Shiksha</option>
              <option value="yellow-pages">Yellow Pages</option>
            </select>
          </div>

          <div className="flex gap-2 items-center">
            <Button size="sm" disabled={currentPage === 1} onClick={() => setCurrentPage(p => p - 1)}>Prev</Button>
            <Button size="sm" disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p + 1)}>Next</Button>
          </div>
        </CardHeader>

        <CardBody className="p-0 overflow-x-auto">
          {loading ? (
            <div className="flex justify-center py-10"><Spinner /></div>
          ) : (
            <table className="w-full min-w-[1500px] table-fixed">
              <thead className="bg-gray-200 sticky top-0">
                <tr>
                  {columns.map((col) => (
                    <th key={col.key} style={{ width: col.width }} className="px-3 py-2">
                      <div onClick={() => toggleSort(col.key)} className="flex gap-2 cursor-pointer">
                        {col.label}
                        <ChevronUpDownIcon className="h-4" />
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pageData.map((row, idx) => (
                  <tr key={idx} className="border-b hover:bg-gray-50">
                    {columns.map((col) => (
                      <td key={col.key} className="px-3 py-3 text-sm break-words">
                        {String(row[col.key] ?? "-")}
                      </td>
                    ))}
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

export default CleanListingMaster;
