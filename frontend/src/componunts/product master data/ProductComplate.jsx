import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Spinner,
  IconButton,
} from "@material-tailwind/react";
import {
  MagnifyingGlassIcon,
  ChevronUpDownIcon,
  ChevronDownIcon,
  ArrowDownTrayIcon,
} from "@heroicons/react/24/solid";
import { productData } from "@/data/productJSON";
import * as XLSX from "xlsx/dist/xlsx.full.min.js";

const defaultColumns = [
  { key: "ASIN", label: "ASIN", width: 150 },
  { key: "Product_name", label: "Product Name", width: 300 },
  { key: "price", label: "Price", width: 100 },
  { key: "rating", label: "Rating", width: 100 },
  { key: "Number_of_ratings", label: "Number of Ratings", width: 120 },
  { key: "Brand", label: "Brand", width: 120 },
  { key: "Seller", label: "Seller", width: 180 },
  { key: "category", label: "Category", width: 180 },
  { key: "category_sub_sub_sub", label: "Category Sub Sub Sub", width: 180 },
  { key: "colour", label: "Colour", width: 100 },
  { key: "size_options", label: "Size Options", width: 150 },
  { key: "description", label: "Description", width: 300 },
  { key: "link", label: "Link", width: 250 },
  { key: "Image_URLs", label: "Image URLs", width: 200 },
  { key: "About_the_items_bullet", label: "About the Items Bullet", width: 250 },
  { key: "Product_details", label: "Product Details", width: 300 },
  { key: "Additional_Details", label: "Additional Details", width: 200 },
  { key: "Manufacturer_Name", label: "Manufacturer Name", width: 180 },
];

// Convert JSON to CSV
const convertToCSV = (arr) => {
  if (!arr.length) return "";
  const headers = Object.keys(arr[0]);
  const rows = arr.map((r) =>
    headers.map((h) => `"${String(r[h] ?? "").replace(/"/g, "'")}"`).join(",")
  );
  return [headers.join(","), ...rows].join("\n");
};

const ProductComplete = () => {
  const [loading, setLoading] = useState(true);
  const [fullData, setFullData] = useState([]);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;

  const [search, setSearch] = useState("");
  const [areaSearch, setAreaSearch] = useState("");

  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  const [columns, setColumns] = useState(defaultColumns);

  // Fetch local product data
  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setFullData(productData);
      setTotal(productData.length);
      setLoading(false);
    }, 300);
  }, []);

  // Filter data
  const filteredData = useMemo(() => {
    let data = [...fullData];

    if (search) {
      data = data.filter((x) =>
        (x.Product_name || "").toLowerCase().includes(search.toLowerCase())
      );
    }

    if (areaSearch) {
      data = data.filter((x) =>
        (x.category || "").toLowerCase().includes(areaSearch.toLowerCase())
      );
    }

    return data;
  }, [fullData, search, areaSearch]);

  // Sort data
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
    if (sortField === field)
      setSortOrder((o) => (o === "asc" ? "desc" : "asc"));
    else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  // Download CSV / Excel
  const downloadCSV = (currentOnly = false) => {
    const arr = currentOnly ? pageData : fullData;
    const csv = convertToCSV(arr);

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = currentOnly ? "page_data.csv" : "all_data.csv";
    a.click();

    URL.revokeObjectURL(url);
  };

  const downloadExcel = (currentOnly = false) => {
    const arr = currentOnly ? pageData : fullData;
    const ws = XLSX.utils.json_to_sheet(arr);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, currentOnly ? "page_data.xlsx" : "all_data.xlsx");
  };

  // Resize Columns
  const startResize = (colKey, e) => {
    e.preventDefault();
    const startX = e.clientX;

    const col = columns.find((c) => c.key === colKey);
    const startWidth = col.width;

    const onMouseMove = (ev) => {
      const delta = ev.clientX - startX;
      const newWidth = Math.max(80, startWidth + delta);

      setColumns((cols) =>
        cols.map((c) => (c.key === colKey ? { ...c, width: newWidth } : c))
      );
    };

    const stop = () => {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", stop);
    };

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", stop);
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4">
      <div className="flex justify-between items-center mb-4">
        <Typography variant="h4">Product Data</Typography>

        <div className="flex items-center gap-2">
          <Button size="sm" onClick={() => downloadCSV(false)}>
            CSV All
          </Button>
          <Button size="sm" onClick={() => downloadCSV(true)}>
            CSV Page
          </Button>
          <Button size="sm" onClick={() => downloadExcel(false)}>
            Excel All
          </Button>
          <Button size="sm" onClick={() => downloadExcel(true)}>
            Excel Page
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader className="flex flex-wrap items-center justify-between gap-3 p-4 bg-gray-100">
          <div className="flex gap-3 items-center flex-wrap">
            <Input
              label="Search Name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <Input
              label="Search Category..."
              value={areaSearch}
              onChange={(e) => setAreaSearch(e.target.value)}
              icon={<MagnifyingGlassIcon className="h-5 w-5" />}
            />
          </div>

          <div className="flex gap-2 items-center">
            <div>
              Page {currentPage} / {totalPages}
            </div>
            <Button
              size="sm"
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            >
              Prev
            </Button>
            <Button
              size="sm"
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </Button>
          </div>
        </CardHeader>

        <CardBody className="p-0 overflow-x-auto">
          {loading ? (
            <div className="flex justify-center py-10">
              <Spinner className="h-10 w-10" />
            </div>
          ) : (
            <table className="w-full table-fixed border-collapse min-w-[1500px]">
              <thead className="sticky top-0 z-20 border-b bg-gray-100">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col.key}
                      style={{ width: col.width }}
                      className="px-3 py-2 text-left relative select-none"
                    >
                      <div className="flex items-center justify-between">
                        <div
                          className="flex items-center gap-2 cursor-pointer"
                          onClick={() => toggleSort(col.key)}
                        >
                          <span className="capitalize text-sm font-semibold">
                            {col.label}
                          </span>

                          {sortField === col.key ? (
                            sortOrder === "asc" ? (
                              <ChevronUpDownIcon className="h-4" />
                            ) : (
                              <ChevronDownIcon className="h-4" />
                            )
                          ) : (
                            <ChevronUpDownIcon className="h-4 opacity-40" />
                          )}
                        </div>

                        <div
                          onMouseDown={(e) => startResize(col.key, e)}
                          className="absolute right-0 top-0 h-full w-2 cursor-col-resize"
                        ></div>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {pageData.length === 0 ? (
                  <tr>
                    <td
                      colSpan={columns.length}
                      className="text-center p-6 text-gray-500"
                    >
                      No records found
                    </td>
                  </tr>
                ) : (
                  pageData.map((row, i) => (
                    <tr key={i} className="border-b hover:bg-gray-50">
                      {columns.map((col) => (
                        <td
                          key={col.key}
                          style={{ width: col.width, maxWidth: col.width }}
                          className="px-3 py-3 break-words text-sm"
                        >
                          {col.key === "link" && row[col.key] ? (
                            <a
                              href={row[col.key]}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-500 underline"
                            >
                              {row[col.key].slice(0, 40)}...
                            </a>
                          ) : (
                            String(row[col.key] ?? "-")
                          )}
                        </td>
                      ))}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>

      <div className="mt-4 flex justify-center items-center gap-2">
        <Button
          size="sm"
          onClick={() => setCurrentPage(1)}
          disabled={currentPage === 1}
        >
          First
        </Button>

        <Button
          size="sm"
          onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
          disabled={currentPage === 1}
        >
          Prev
        </Button>

        <div className="px-3 py-1 border rounded">
          Page {currentPage} / {totalPages}
        </div>

        <Button
          size="sm"
          onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
          disabled={currentPage === totalPages}
        >
          Next
        </Button>

        <Button
          size="sm"
          onClick={() => setCurrentPage(totalPages)}
          disabled={currentPage === totalPages}
        >
          Last
        </Button>
      </div>
    </div>
  );
};

export default ProductComplete;
