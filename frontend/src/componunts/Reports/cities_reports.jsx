import React, { useMemo, useState } from "react";
import {
  Card,
  CardBody,
  Typography,
} from "@material-tailwind/react";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import { listingData } from "@/data/listingJSON";

export function CitiesSummary() {
  const [selectedCategory, setSelectedCategory] = useState("Cafe"); 
  const [citySearch, setCitySearch] = useState("");

  // 1. Get List of Unique Categories
  const uniqueCategories = useMemo(() => {
    return [...new Set(listingData.map((item) => item.category))].filter(Boolean).sort();
  }, []);

  // 2. Get List of Unique Cities
  const uniqueCities = useMemo(() => {
    return [...new Set(listingData.map((item) => item.city))].filter(Boolean).sort();
  }, []);

  // 3. Process Rows
  const tableRows = useMemo(() => {
    let cities = uniqueCities;
    if (citySearch) {
      cities = cities.filter(city => 
        city.toLowerCase().includes(citySearch.toLowerCase())
      );
    }

    return cities.map(city => {
      const count = listingData.filter(item => 
        item.city === city && 
        (selectedCategory === "All" ? true : item.category === selectedCategory)
      ).length;

      return {
        city,
        category: selectedCategory === "All" ? "All Categories" : selectedCategory,
        count
      };
    });
  }, [uniqueCities, citySearch, selectedCategory]);

  // --- UPDATED STYLING FOR LIGHT THEME ---
  
  // Input: White background, gray border, subtle shadow
  const headerInputClass = "w-full bg-white text-gray-700 placeholder-gray-400 border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-gray-100 focus:border-blue-gray-300 transition-all shadow-sm";
  
  // Select: White background, gray border, bold text
  const headerSelectClass = "w-full bg-white text-gray-800 border border-gray-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-gray-100 focus:border-blue-gray-300 cursor-pointer font-bold uppercase shadow-sm";

  return (
    <div className="mt-8 mb-12 px-4 max-w-5xl mx-auto">
      
      <div className="mb-4">
        <Typography variant="h4" color="blue-gray" className="font-bold">
          Live Data Grid
        </Typography>
        <Typography variant="small" className="text-gray-500">
          Professional view of listing distribution.
        </Typography>
      </div>

      <Card className="border border-gray-300 shadow-sm overflow-hidden rounded-lg">
        <CardBody className="p-0 overflow-visible">
          <table className="w-full text-left table-fixed border-collapse">
            
            {/* --- PROFESSIONAL LIGHT HEADER --- */}
            {/* Gradient: White -> Very Light Gray (Gray-100) */}
            <thead className="bg-gradient-to-b from-white to-gray-100 border-b border-gray-300">
              <tr>
                
                {/* COL 1: CITY FILTER */}
                <th className="px-4 py-3 w-1/3 align-top border-r border-gray-200">
                  <div className="flex flex-col gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-gray-500 flex items-center gap-1">
                      Filter by City
                    </span>
                    <div className="relative">
                        <MagnifyingGlassIcon className="absolute left-2 top-2 h-3.5 w-3.5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search..."
                            value={citySearch}
                            onChange={(e) => setCitySearch(e.target.value)}
                            className={`${headerInputClass} pl-8`}
                        />
                    </div>
                  </div>
                </th>

                {/* COL 2: CATEGORY DROPDOWN */}
                <th className="px-4 py-3 w-1/3 align-top border-r border-gray-200 bg-gray-50/50">
                  <div className="flex flex-col gap-2">
                    {/* Text is Blue-Gray to indicate it's active/selectable */}
                    <span className="text-[11px] font-bold uppercase tracking-wider text-blue-gray-600">
                      Select Category ▼
                    </span>
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className={headerSelectClass}
                    >
                      <option value="All">All Categories</option>
                      {uniqueCategories.map((cat) => (
                        <option key={cat} value={cat}>
                          {cat}
                        </option>
                      ))}
                    </select>
                  </div>
                </th>

                {/* COL 3: COUNT LABEL */}
                <th className="px-4 py-3 w-1/3 align-middle">
                   <div className="flex flex-col items-center justify-center h-full">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-gray-500">
                      Total Data
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
                    No cities found matching "{citySearch}"
                  </td>
                </tr>
              ) : (
                tableRows.map((row, index) => (
                  <tr 
                    key={row.city} 
                    className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
                  >
                    {/* City Name */}
                    <td className="px-4 py-3 font-semibold text-gray-900 border-r border-gray-100">
                      {row.city}
                    </td>

                    {/* Category Name */}
                    <td className="px-4 py-3 text-gray-500 border-r border-gray-100 bg-gray-50/30">
                      {row.category}
                    </td>

                    {/* Count - Dark badge for contrast */}
                    <td className="px-4 py-3 text-center">
                        <span className="inline-block px-3 py-1 bg-gray-100 text-gray-800 rounded-full font-bold text-xs border border-gray-200">
                           {row.count}
                        </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
            
            {/* FOOTER - LIGHT THEME */}
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

export default CitiesSummary;