import React from 'react';
import { Card, CardHeader, Typography, CardBody } from "@material-tailwind/react";

const DataTable = ({ title, columns, data, color = "blue-gray" }) => {
  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Card>
        <CardHeader variant="gradient" color={color} className="mb-8 p-6">
          <Typography variant="h6" color="white">
            {title}
          </Typography>
        </CardHeader>
        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <table className="w-full min-w-[640px] table-auto">
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col.header} className="border-b border-blue-gray-50 py-3 px-5 text-left whitespace-nowrap">
                    <Typography variant="small" className="text-[11px] font-bold uppercase text-blue-gray-400">
                      {col.header}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((item, rowIndex) => (
                <tr key={rowIndex}>
                  {columns.map((col, colIndex) => {
                    const className = `py-3 px-5 ${rowIndex === data.length - 1 ? "" : "border-b border-blue-gray-50"}`;
                    return (
                      <td key={colIndex} className={className}>
                        {col.render ? (
                          col.render(item)
                        ) : (
                          <Typography className="text-xs font-semibold text-blue-gray-600 whitespace-nowrap">
                            {item[col.accessor] || "-"}
                          </Typography>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </CardBody>
      </Card>
    </div>
  );
};

export default DataTable;