import React, { useMemo, useState } from "react";
import {
  Card,
  CardBody,
  Typography,
} from "@material-tailwind/react";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import { listingData } from "@/data/listingJSON";

export function CategoriesReports() {
  const [selectedCity, setSelectedCity] = useState("All"); 
  const [categorySearch, setCategorySearch] = useState("");

  // 1. Get List of Unique Cities for the Header Dropdown
  const uniqueCities = useMemo(() => {
    return [...new Set(listingData.map((item) => item.city))].filter(Boolean).sort();
  }, []);

  // 2. Get List of Unique Categories (Rows)
  const uniqueCategories = useMemo(() => {
    return [...new Set(listingData.map((item) => item.category))].filter(Boolean).sort();
  }, []);

  // 3. Process Rows: Filter Categories -> Calculate Count for Selected City
  const tableRows = useMemo(() => {
    // A. Filter categories based on search input
    let categories = uniqueCategories;
    if (categorySearch) {
      categories = categories.filter(cat => 
        cat.toLowerCase().includes(categorySearch.toLowerCase())
      );
    }

    // B. Map to row data
    return categories.map(category => {
      // Calculate count for this Category AND the selected City
      const count = listingData.filter(item => 
        item.category === category && 
        (selectedCity === "All" ? true : item.city === selectedCity)
      ).length;

      return {
        category,
        city: selectedCity === "All" ? "All Cities" : selectedCity,
        count
      };
    });
  }, [uniqueCategories, categorySearch, selectedCity]);

  // --- STYLING (Light Professional Theme) ---
  const headerInputClass = "w-full bg-white text-gray-700 placeholder-gray-400 border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-gray-100 focus:border-blue-gray-300 transition-all shadow-sm";
  const headerSelectClass = "w-full bg-white text-gray-800 border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-gray-100 focus:border-blue-gray-300 cursor-pointer font-bold uppercase shadow-sm";

  return (
    <div className="mt-8 mb-12 px-4 max-w-5xl mx-auto">
      
      <div className="mb-4">
        <Typography variant="h4" color="blue-gray" className="font-bold">
          Category Data Grid
        </Typography>
        <Typography variant="small" className="text-gray-500">
          Analyze listing distribution by industry category.
        </Typography>
      </div>

      <Card className="border border-gray-300 shadow-sm overflow-hidden rounded-lg">
        <CardBody className="p-0 overflow-visible">
          <table className="w-full text-left table-fixed border-collapse">
            
            {/* --- PROFESSIONAL LIGHT HEADER --- */}
            <thead className="bg-gradient-to-b from-white to-gray-100 border-b border-gray-300">
              <tr>
                
                {/* COL 1: CATEGORY FILTER (Search) */}
                <th className="px-4 py-3 w-1/3 align-top border-r border-gray-200">
                  <div className="flex flex-col gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-gray-500 flex items-center gap-1">
                      Filter Category
                    </span>
                    <div className="relative">
                        <MagnifyingGlassIcon className="absolute left-2 top-2 h-3.5 w-3.5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search..."
                            value={categorySearch}
                            onChange={(e) => setCategorySearch(e.target.value)}
                            className={`${headerInputClass} pl-8`}
                        />
                    </div>
                  </div>
                </th>

                {/* COL 2: CITY DROPDOWN (The Pivot) */}
                <th className="px-4 py-3 w-1/3 align-top border-r border-gray-200 bg-gray-50/50">
                  <div className="flex flex-col gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-blue-gray-600">
                      Select City ▼
                    </span>
                    <select
                      value={selectedCity}
                      onChange={(e) => setSelectedCity(e.target.value)}
                      className={headerSelectClass}
                    >
                      <option value="All">All Cities</option>
                      {uniqueCities.map((city) => (
                        <option key={city} value={city}>
                          {city}
                        </option>
                      ))}
                    </select>
                  </div>
                </th>

                {/* COL 3: COUNT LABEL */}
                <th className="px-4 py-3 w-1/3 align-middle">
                   <div className="flex flex-col items-center justify-center h-full">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-gray-500">
                      Total Listings
                    </span>
                    <span className="text-[10px] text-gray-400 font-normal mt-0.5">
                      (Live Updates)
                    </span>
                   </div>
                </th>

              </tr>
            </thead>

            {/* --- TABLE BODY --- */}
            <tbody className="text-sm text-gray-700 bg-white">
              {tableRows.length === 0 ? (
                <tr>
                  <td colSpan={3} className="px-6 py-12 text-center text-gray-400 italic bg-gray-50">
                    No categories found matching "{categorySearch}"
                  </td>
                </tr>
              ) : (
                tableRows.map((row) => (
                  <tr 
                    key={row.category} 
                    className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
                  >
                    {/* Category Name */}
                    <td className="px-4 py-3 font-semibold text-gray-900 border-r border-gray-100">
                      {row.category}
                    </td>

                    {/* City Name (Repeats based on selection) */}
                    <td className="px-4 py-3 text-gray-500 border-r border-gray-100 bg-gray-50/30">
                      {row.city}
                    </td>

                    {/* Count */}
                    <td className="px-4 py-3 text-center">
                        <span className={`inline-block px-3 py-1 rounded-full font-bold text-xs border ${
                            row.count > 0 
                            ? "bg-gray-100 text-gray-800 border-gray-200" 
                            : "bg-transparent text-gray-300 border-transparent"
                        }`}>
                           {row.count}
                        </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
            
            {/* FOOTER */}
            <tfoot className="bg-gray-50 font-bold text-gray-800 border-t border-gray-300">
                <tr>
                    <td className="px-4 py-2.5 text-xs uppercase text-gray-500">
                        Total Rows: {tableRows.length}
                    </td>
                    <td className="px-4 py-2.5 border-l border-gray-200"></td>
                    <td className="px-4 py-2.5 text-center border-l border-gray-200 text-blue-gray-900">
                        {tableRows.reduce((sum, row) => sum + row.count, 0)}
                    </td>
                </tr>
            </tfoot>

          </table>
        </CardBody>
      </Card>
    </div>
  );
}

export default CategoriesReports;