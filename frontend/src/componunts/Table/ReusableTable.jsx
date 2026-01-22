import React from 'react';
import './TableStyle.css'; 

const ReusableTable = ({ columns, data }) => {
  if (!data || data.length === 0) return <div className="no-data">No data available</div>;

  return (
    <div className="table-wrapper">
      <table className="custom-table">
        <thead>
          <tr>
            {columns.map((col, index) => (
              <th key={index}>{col.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((col, colIndex) => (
                <td key={colIndex}>
                  {/* Checks if there is a custom render function (for images/buttons) */}
                  {col.render 
                    ? col.render(row) 
                    : row[col.accessor]
                  }
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ReusableTable;