import React, { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import Service from './Service'

export default function ProductIndex() {
  const [products, setProducts] = useState([])
  const location = useLocation()

  useEffect(() => {
    fetchProducts()
  }, [location])

  const fetchProducts = () => {
    Service.get()
      .then(res => setProducts(res.data))
      .catch(err => alert("Failed to fetch products: " + err.response?.data || err.message))
  }

  return (
    <div className="container py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">📦 Product List</h2>
        <Link className="btn btn-success" to="/product/create">
          <i className="fa fa-plus me-2"></i> Add Product
        </Link>
      </div>

      <div className="table-responsive">
        <table className="table table-bordered align-middle table-hover shadow-sm">
          <thead className="table-light">
            <tr className="text-center">
              <th>#</th>
              <th>Name</th>
              <th>Price (₹)</th>
              <th style={{ width: '160px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.length > 0 ? (
              products.map(product => (
                <tr key={product.id} className="text-center">
                  <td>{product.id}</td>
                  <td className="text-start">{product.name}</td>
                  <td>{product.price}</td>
                  <td>
                    <Link to={`/product/${product.id}`} className="btn btn-outline-secondary btn-sm me-1" title="View">
                      <i className="fa fa-eye"></i>
                    </Link>
                    <Link to={`/product/edit/${product.id}`} className="btn btn-outline-primary btn-sm me-1" title="Edit">
                      <i className="fa fa-edit"></i>
                    </Link>
                    <Link to={`/product/delete/${product.id}`} className="btn btn-outline-danger btn-sm" title="Delete">
                      <i className="fa fa-trash"></i>
                    </Link>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center text-muted">No products found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
