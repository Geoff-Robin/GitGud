import React, { useState } from "react";
import "./ProblemEntryPage.css";
import Navbar from "@/components/ui/navbar";

function ProblemEntryPage() {
  // Track which forms are open
  const [openForms, setOpenForms] = useState({
    form1: false,
    form2: false,
    form3: false,
    form4: false,
    form5: false
  });
  
  // Form input values
  const [formData, setFormData] = useState({
    form1: { topic: "", url: "" },
    form2: { topic: "", url: "" },
    form3: { topic: "", url: "" },
    form4: { topic: "", url: "" },
    form5: { topic: "", url: "" }
  });

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 6; // Total number of pages
  
  // Toggle form visibility
  const toggleForm = (formId) => {
    // Close any open forms
    const updatedForms = Object.keys(openForms).reduce((acc, key) => {
      acc[key] = key === formId ? !openForms[formId] : false;
      return acc;
    }, {});
    
    setOpenForms(updatedForms);
  };
  
  // Handle input changes
  const handleInputChange = (formId, field, value) => {
    setFormData(prev => ({
      ...prev,
      [formId]: {
        ...prev[formId],
        [field]: value
      }
    }));
  };
  
  // Handle form submission
  const handleSubmit = (formId) => {
    const data = formData[formId];
    console.log(`Form ${formId} submitted on page ${currentPage}:`, data);
    
    // Reset form and close it
    setFormData(prev => ({
      ...prev,
      [formId]: { topic: "", url: "" }
    }));
    
    toggleForm(formId);
    
    // In a real app, you would send this data to your backend
    alert(`Problem submitted on page ${currentPage}!\nTopic: ${data.topic}\nURL: ${data.url}`);
  };

  // Handle page navigation
  const goToPage = (pageNumber) => {
    // Close any open forms when changing pages
    setOpenForms({
      form1: false,
      form2: false,
      form3: false,
      form4: false,
      form5: false
    });
    
    setCurrentPage(pageNumber);
  };

  // Go to next page
  const nextPage = () => {
    if (currentPage < totalPages) {
      goToPage(currentPage + 1);
    }
  };

  // Go to previous page
  const prevPage = () => {
    if (currentPage > 1) {
      goToPage(currentPage - 1);
    }
  };
  
  // Find if any form is currently open
  const activeForm = Object.keys(openForms).find(key => openForms[key]) || null;
  
  // Generate pagination numbers
  const renderPaginationNumbers = () => {
    const pages = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => goToPage(i)}
          className={`page-number ${currentPage === i ? 'active' : ''}`}
        >
          {i}
        </button>
      );
    }
    return pages;
  };
  
  return (
    <>
      <Navbar />
      <div className="problem-entry-container">
        <h1 className="page-title">Problem Entry Page {currentPage}</h1>
        
        {/* Horizontal buttons row */}
        <div className="buttons-row">
          {[1, 2, 3, 4, 5].map(num => {
            const formId = `form${num}`;
            return (
              <button
                key={formId}
                onClick={() => toggleForm(formId)}
                className={`add-button ${openForms[formId] ? 'active' : ''}`}
              >
                <span className="plus-icon">+</span>
                Add Problem {num}
              </button>
            );
          })}
        </div>
        
        {/* Form display area */}
        {activeForm && (
          <div className="form-container">
            <div className="form-header">
              <h3 className="form-title">
                Add Problem {activeForm.replace("form", "")} (Page {currentPage})
              </h3>
              <button 
                onClick={() => toggleForm(activeForm)} 
                className="close-button"
              >
                ×
              </button>
            </div>
            
            <div className="form-fields">
              <div className="form-group">
                <label htmlFor={`${activeForm}-topic`}>
                  Problem Topic
                </label>
                <input
                  id={`${activeForm}-topic`}
                  type="text"
                  value={formData[activeForm].topic}
                  onChange={(e) => handleInputChange(activeForm, "topic", e.target.value)}
                  placeholder="Enter problem topic"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor={`${activeForm}-url`}>
                  Problem URL
                </label>
                <input
                  id={`${activeForm}-url`}
                  type="text"
                  value={formData[activeForm].url}
                  onChange={(e) => handleInputChange(activeForm, "url", e.target.value)}
                  placeholder="Enter problem URL"
                />
              </div>
              
              <button
                onClick={() => handleSubmit(activeForm)}
                className="submit-button"
              >
                Submit
              </button>
            </div>
          </div>
        )}
        
        {/* Pagination controls */}
        <div className="pagination-container">
          <button 
            onClick={prevPage} 
            className="pagination-button"
            disabled={currentPage === 1}
          >
            &laquo; Previous
          </button>
          
          <div className="pagination-numbers">
            {renderPaginationNumbers()}
          </div>
          
          <button 
            onClick={nextPage} 
            className="pagination-button"
            disabled={currentPage === totalPages}
          >
            Next &raquo;
          </button>
        </div>
      </div>
    </>
  );
}

export default ProblemEntryPage;