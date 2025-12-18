import {
  Card,
  CardBody,
  CardHeader,
  Chip,
  Input,
  Typography,
} from "@material-tailwind/react";
import React, { useEffect, useState } from "react";

// Import local data
import { authorsTableData } from "@/data/authors-table-data";

const ServiceCategory = () => {
  const [data, setData] = useState(authorsTableData);
  const [search, setSearch] = useState("");

  useEffect(() => {
    filterData(search);
  }, [search]);

  const filterData = (searchTerm) => {
    if (!searchTerm) {
      setData(authorsTableData);
      return;
    }

    const filtered = authorsTableData.filter((item) =>
      (item.name || "").toLowerCase().includes(searchTerm.toLowerCase())
    );

    setData(filtered);
  };

  return (
    <div className="mt-12 mb-8 flex flex-col gap-12">
      <Card>
        <CardHeader
          variant="gradient"
          color="gray"
          className="mb-6 p-6 flex justify-between items-center"
        >
          <Typography variant="h6" color="white">
            Service Category
          </Typography>

          <Input
            label="Search author..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-white rounded"
          />
        </CardHeader>

        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          {data.length === 0 ? (
            <div className="text-center py-8 text-gray-600">
              No matching records
            </div>
          ) : (
            <table className="w-full min-w-[640px] table-auto">
              <thead>
                <tr>
                  {["Author", "Function", "Status", "Employed", ""].map((el) => (
                    <th
                      key={el}
                      className="border-b border-blue-gray-50 py-3 px-5 text-left"
                    >
                      <Typography
                        variant="small"
                        className="text-[11px] font-bold uppercase text-blue-gray-400"
                      >
                        {el}
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {data.map(({ img, name, email, job, online, date }, idx) => {
                  const className = `py-3 px-5 ${
                    idx === data.length - 1
                      ? ""
                      : "border-b border-blue-gray-50"
                  }`;

                  return (
                    <tr key={name + idx}>
                      {/* Author */}
                      <td className={className}>
                        <div className="flex items-center gap-4">
                          <img
                            src={img}
                            alt={name}
                            className="w-10 h-10 rounded-md object-cover"
                          />

                          <div>
                            <Typography
                              variant="small"
                              className="font-semibold text-blue-gray-700"
                            >
                              {name}
                            </Typography>

                            <Typography className="text-xs text-blue-gray-500">
                              {email}
                            </Typography>
                          </div>
                        </div>
                      </td>

                      {/* Job */}
                      <td className={className}>
                        <Typography className="text-xs font-semibold text-blue-gray-700">
                          {job[0]}
                        </Typography>
                        <Typography className="text-xs text-blue-gray-500">
                          {job[1]}
                        </Typography>
                      </td>

                      {/* Status */}
                      <td className={className}>
                        <Chip
                          variant="gradient"
                          color={online ? "green" : "red"}
                          value={online ? "online" : "offline"}
                          className="py-0.5 px-2 text-[11px] font-medium w-fit"
                        />
                      </td>

                      {/* Employed date */}
                      <td className={className}>
                        <Typography className="text-xs font-semibold text-blue-gray-700">
                          {date}
                        </Typography>
                      </td>

                      {/* Edit */}
                      <td className={className}>
                        <Typography
                          as="a"
                          href="#"
                          className="text-xs font-semibold text-blue-gray-600"
                        >
                          Edit
                        </Typography>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>
    </div>
  );
};

export default ServiceCategory;
