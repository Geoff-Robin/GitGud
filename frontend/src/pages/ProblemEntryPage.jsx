import React, { useState } from 'react';
import "../ProblemEntryPage.css";
import Navbar from '@/components/ui/navbar';

const PopulatedProblemGridDemo = () => {
  // Sample data for demonstration (8 problems instead of 9)
  const problemData = [
    { name: "Two Sum", url: "https://leetcode.com/problems/two-sum/" },
    { name: "Add Two Numbers", url: "https://leetcode.com/problems/add-two-numbers/" },
    { name: "Longest Substring Without Repeating Characters", url: "https://leetcode.com/problems/longest-substring-without-repeating-characters/" },
    { name: "Median of Two Sorted Arrays", url: "https://leetcode.com/problems/median-of-two-sorted-arrays/" },
    { name: "Longest Palindromic Substring", url: "https://leetcode.com/problems/longest-palindromic-substring/" },
    { name: "Zigzag Conversion", url: "https://leetcode.com/problems/zigzag-conversion/" },
    { name: "Reverse Integer", url: "https://leetcode.com/problems/reverse-integer/" },
    { name: "String to Integer (atoi)", url: "https://leetcode.com/problems/string-to-integer-atoi/" }
  ];

  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 6;
  const GRID_SIZE = 9;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [hoveredCell, setHoveredCell] = useState(null);

  // Open the URL input modal
  const openUrlModal = () => {
    setIsModalOpen(true);
  };

  // Close the URL input modal
  const closeUrlModal = () => {
    setIsModalOpen(false);
  };

  // Navigate to previous page
  const goToPrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  // Navigate to next page
  const goToNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  // Function to render pagination numbers with ellipsis for large page counts
  const renderPaginationNumbers = () => {
    const paginationItems = [];
    
    // Always show first page
    paginationItems.push(
      <button 
        key={1} 
        className={`url-grid-pagination-number ${currentPage === 1 ? 'active' : ''}`}
        onClick={() => setCurrentPage(1)}
      >
        1
      </button>
    );
    
    // Logic for showing ellipsis and surrounding pages
    if (totalPages > 5) {
      if (currentPage > 3) {
        paginationItems.push(
          <span key="ellipsis-1" className="url-grid-pagination-ellipsis">...</span>
        );
      }
      
      // Show current page and surrounding pages
      const startPage = Math.max(2, currentPage - 1);
      const endPage = Math.min(totalPages - 1, currentPage + 1);
      
      for (let i = startPage; i <= endPage; i++) {
        if (i !== 1 && i !== totalPages) {
          paginationItems.push(
            <button 
              key={i} 
              className={`url-grid-pagination-number ${currentPage === i ? 'active' : ''}`}
              onClick={() => setCurrentPage(i)}
            >
              {i}
            </button>
          );
        }
      }
      
      if (currentPage < totalPages - 2) {
        paginationItems.push(
          <span key="ellipsis-2" className="url-grid-pagination-ellipsis">...</span>
        );
      }
    } else {
      // Show all pages if there aren't many
      for (let i = 2; i < totalPages; i++) {
        paginationItems.push(
          <button 
            key={i} 
            className={`url-grid-pagination-number ${currentPage === i ? 'active' : ''}`}
            onClick={() => setCurrentPage(i)}
          >
            {i}
          </button>
        );
      }
    }
    
    // Always show last page
    if (totalPages > 1) {
      paginationItems.push(
        <button 
          key={totalPages} 
          className={`url-grid-pagination-number ${currentPage === totalPages ? 'active' : ''}`}
          onClick={() => setCurrentPage(totalPages)}
        >
          {totalPages}
        </button>
      );
    }
    
    return paginationItems;
  };

  return (
    <div className="flex flex-col">
      <Navbar />
      <div className="url-grid-page">
        <div className="url-grid-wrapper">
          <div className="url-grid-container">
            <div className="url-grid-header">
              <h2>Problems</h2>
              <div className="url-grid-page-indicator">Page {currentPage} of {totalPages}</div>
            </div>
            
            <div className="url-grid">
              {Array(GRID_SIZE).fill(null).map((_, index) => {
                // The last cell (index 8) will be the add button
                const isAddButton = index === 8;
                const problem = isAddButton ? null : problemData[index];

                return (
                  <div 
                    key={index}
                    className={`url-grid-cell ${hoveredCell === index ? 'url-grid-cell-hover' : ''}`}
                    onMouseEnter={() => setHoveredCell(index)}
                    onMouseLeave={() => setHoveredCell(null)}
                  >
                    {isAddButton ? (
                      <button 
                        className="url-grid-add-button"
                        onClick={openUrlModal}
                      >
                        <span className="plus-icon">+</span>
                      </button>
                    ) : (
                      <div className="url-grid-url-display">
                        <div className="url-grid-problem-name">{problem.name}</div>
                        <div className="url-grid-url-text">{problem.url}</div>
                        <div className="url-grid-url-favicon">
                          <div className="favicon-placeholder"></div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
            
            <div className="url-grid-pagination">
              <button 
                className={`url-grid-pagination-nav ${currentPage === 1 ? 'disabled' : ''}`}
                onClick={goToPrevPage}
                disabled={currentPage === 1}
              >
                <span className="nav-icon">←</span> Prev
              </button>
              
              <div className="url-grid-pagination-numbers">
                {renderPaginationNumbers()}
              </div>
              
              <button 
                className={`url-grid-pagination-nav ${currentPage === totalPages ? 'disabled' : ''}`}
                onClick={goToNextPage}
                disabled={currentPage === totalPages}
              >
                Next <span className="nav-icon">→</span>
              </button>
            </div>
          </div>
        </div>

        {isModalOpen && (
          <div className="url-grid-modal" onClick={(e) => {
            if (e.target === e.currentTarget) closeUrlModal();
          }}>
            <div className="url-grid-modal-content">
              <h3>Add Problem URL</h3>
              <div className="url-grid-form-group">
                <input 
                  type="text"
                  placeholder="Enter Problem Name" 
                  autoFocus
                />
                <input 
                  type="url" 
                  placeholder="Enter leetcode problem URL" 
                />
              </div>
              <div className="url-grid-buttons">
                <button className="url-grid-btn url-grid-btn-cancel" onClick={closeUrlModal}>Cancel</button>
                <button className="url-grid-btn url-grid-btn-submit">Submit</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PopulatedProblemGridDemo;