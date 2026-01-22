import React, { useState, useEffect } from 'react';
import { Card, CardHeader, Typography, CardBody, Chip } from "@material-tailwind/react";
import { fetchZomatoData } from '../../Service/listingService'; // Ensure this path matches your working Amazon file

export default function ZomatoData() {
  const [tableData, setTableData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        // Calling the Zomato service we added earlier
        const data = await fetchZomatoData();
        setTableData(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error(err);
        setError("Waiting for Backend connection...");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div className="p-4 font-bold text-red-500">Connecting to Zomato Database...</div>;
  if (error) return <div className="p-4 text-red-500 font-bold">Status: {error}</div>;

  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Card>
        <CardHeader variant="gradient" color="red" className="mb-8 p-6">
          <Typography variant="h6" color="white">
            Zomato Product Master
          </Typography>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <table className="w-full min-w-[640px] table-auto">
            <thead>
              <tr>
                {/* Adjust headers based on what Zomato data looks like */}
                {["Restaurant Name", "Location", "Cuisine", "Rating", "Status"].map((el) => (
                  <th key={el} className="border-b border-blue-gray-50 py-3 px-5 text-left">
                    <Typography variant="small" className="text-[11px] font-bold uppercase text-blue-gray-400">
                      {el}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((item, key) => {
                const className = `py-3 px-5 ${key === tableData.length - 1 ? "" : "border-b border-blue-gray-50"}`;

                return (
                  <tr key={key}>
                    <td className={className}>
                      <Typography className="text-xs font-semibold text-blue-gray-600">
                        {item.name || item.restaurant_name || "N/A"}
                      </Typography>
                    </td>
                    <td className={className}>
                      <Typography className="text-xs font-semibold text-blue-gray-600">
                        {item.location || item.address || "N/A"}
                      </Typography>
                    </td>
                    <td className={className}>
                      <Typography className="text-xs font-semibold text-blue-gray-600">
                        {item.cuisine || "N/A"}
                      </Typography>
                    </td>
                    <td className={className}>
                      <Typography className="text-xs font-semibold text-blue-gray-600">
                        {item.rating || "-"}
                      </Typography>
                    </td>
                    <td className={className}>
                      <Chip
                        variant="ghost"
                        size="sm"
                        value={item.name ? "Active" : "Pending"}
                        color="green"
                      />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </CardBody>
      </Card>
    </div>
  );
}