import React, { useState, useEffect } from 'react';
import ReusableTable from '../Table/ReusableTable';
import api from '../../utils/Api';

const MasterDataRegistry = () => {
  const [allData, setAllData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Pagination States
  const [currentPage, setCurrentPage] = useState(1);
  const [nextCursor, setNextCursor] = useState(null);
  const [prevCursors, setPrevCursors] = useState([]); // stack for previous cursors

  const columns = [
    { header: "Global ID", accessor: "global_business_id" },
    { header: "Business ID", accessor: "business_id" },
    { header: "Business Name", accessor: "business_name" },
    { header: "Category", accessor: "business_category" },
    { header: "Subcategory", accessor: "business_subcategory" },
    { header: "Ratings", accessor: "ratings" },
    { header: "Reviews", accessor: "reviews" },
    { header: "Primary Phone", accessor: "primary_phone" },
    { header: "Secondary Phone", accessor: "secondary_phone" },
    { header: "Other Phones", accessor: "other_phones" },
    { header: "Virtual Phone", accessor: "virtual_phone" },
    { header: "WhatsApp", accessor: "whatsapp_phone" },
    { header: "Email", accessor: "email" },
    {
      header: "Website",
      accessor: "website_url",
      render: (row) => row.website_url ? <a href={row.website_url} target="_blank" rel="noreferrer">Link</a> : "-"
    },
    {
      header: "Facebook",
      accessor: "facebook_url",
      render: (row) => row.facebook_url ? <a href={row.facebook_url} target="_blank" rel="noreferrer">FB</a> : "-"
    },
    {
      header: "LinkedIn",
      accessor: "linkedin_url",
      render: (row) => row.linkedin_url ? <a href={row.linkedin_url} target="_blank" rel="noreferrer">LI</a> : "-"
    },
    {
      header: "Twitter",
      accessor: "twitter_url",
      render: (row) => row.twitter_url ? <a href={row.twitter_url} target="_blank" rel="noreferrer">X</a> : "-"
    },
    { header: "Address", accessor: "address" },
    { header: "Area", accessor: "area" },
    { header: "City", accessor: "city" },
    { header: "State", accessor: "state" },
    { header: "Pincode", accessor: "pincode" },
    { header: "Country", accessor: "country" },
    { header: "Latitude", accessor: "latitude" },
    { header: "Longitude", accessor: "longitude" },
    { header: "Avg Fees", accessor: "avg_fees" },
    { header: "Course Details", accessor: "course_details" },
    { header: "Duration", accessor: "duration" },
    { header: "Requirement", accessor: "requirement" },
    { header: "Avg Spent", accessor: "avg_spent" },
    { header: "Cost for Two", accessor: "cost_for_two" },
    { header: "Description", accessor: "description" },
    { header: "Data Source", accessor: "data_source" },
    { header: "Avg Salary", accessor: "avg_salary" },
    { header: "Admission Req", accessor: "admission_req_list" },
    { header: "Courses", accessor: "courses" }
  ];

  useEffect(() => {
    setCurrentPage(1);
    setPrevCursors([]);
    fetchData(null, 'init');
    // eslint-disable-next-line
  }, []);

  const fetchData = (cursor = null, direction = 'next') => {
    setLoading(true);
    const params = { limit: 10 };
    if (cursor) params.cursor = cursor;
    api.get(`/master_table/table`, { params })
      .then(res => {
        const result = res.data;
        setAllData(result.data || []);
        setNextCursor(result.next_cursor || null);
        if (direction === 'next') {
          setPrevCursors(prev => cursor ? [...prev, cursor] : prev);
          setCurrentPage(prev => prev + 1);
        } else if (direction === 'prev') {
          setCurrentPage(prev => (prev > 1 ? prev - 1 : 1));
        } else if (direction === 'init') {
          setCurrentPage(1);
          setPrevCursors([]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };
  return (
    <div style={{ padding: '20px' }}>
      <h2>Full Master Registry (All 36 Fields)</h2>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Complete Master Registry</h2>
        {allData && allData.length > 0 && (
          <span style={{ fontSize: '14px', color: '#666' }}>Total Records: {allData.length}</span>
        )}
      </div>

      {loading ? (
        <p>Fetching massive dataset...</p>
      ) : (
        <>
          <ReusableTable columns={columns} data={allData} />

          {/* PAGINATION CONTROLS */}
          <div style={{
            marginTop: '20px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: '15px'
          }}>
            <button
              disabled={currentPage === 1 || prevCursors.length === 0}
              onClick={() => {
                const prevCursor = prevCursors[prevCursors.length - 2] || null;
                setPrevCursors(prev => prev.slice(0, -1));
                fetchData(prevCursor, 'prev');
              }}
              style={{ padding: '5px 15px', cursor: currentPage === 1 ? 'not-allowed' : 'pointer' }}
            >
              Previous
            </button>

            <span style={{ fontWeight: 'bold' }}>
              Page {currentPage}
            </span>

            <button
              disabled={!nextCursor}
              onClick={() => fetchData(nextCursor, 'next')}
              style={{ padding: '5px 15px', cursor: !nextCursor ? 'not-allowed' : 'pointer' }}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default MasterDataRegistry;