import React, { useState, useEffect } from 'react';
import ReusableTable from '../Table/ReusableTable'; 

const BlinkitData = () => { 
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const columns = [
    { 
      header: "Image", 
      accessor: "img", // CHANGE THIS to match your backend key (e.g. 'image_url')
      render: (row) => (
        <img 
          src={row.img} // CHANGE THIS to match your backend key
          alt="product" 
          style={{ width: "50px", height: "50px", objectFit: "contain" }} 
        />
      )
    },
    { 
      header: "Product Name", 
      accessor: "name", // CHANGE THIS to match your backend key (e.g. 'product_name')
      render: (row) => (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontWeight: 'bold' }}>{row.name}</span> 
          <span style={{ fontSize: '11px', color: '#666' }}>ID: {row.id}</span>
        </div>
      )
    },
    { 
      header: "Price", 
      accessor: "price", // CHANGE THIS to match your backend key
      render: (row) => (
        <span style={{ fontWeight: 'bold' }}>₹{row.price}</span>
      )
    },
    { 
      header: "Stock", 
      accessor: "stock_status", // CHANGE THIS (or delete this block if you don't have stock data)
      render: (row) => (
        <span style={{ 
          color: row.stock_status === 'In Stock' ? 'green' : 'red', 
          fontSize: '12px' 
        }}>
          {row.stock_status}
        </span>
      )
    },
    {
      header: "Action",
      accessor: "action",
      render: (row) => (
        <button 
           style={{ padding: '5px 10px', cursor: 'pointer' }}
           onClick={() => alert(`Clicked ${row.name}`)}
        >
          View
        </button>
      )
    }
  ];

  useEffect(() => {
    fetch('http://localhost:5000/api/flipkart-products') // CHANGE THIS URL to your specific API endpoint
      .then((response) => response.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Blinkit Product Master</h2> 
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ReusableTable columns={columns} data={products} />
      )}
    </div>
  );
};

export default BlinkitData;