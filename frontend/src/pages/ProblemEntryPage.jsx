import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '@/components/ui/navbar'; // Import your existing Navbar component
import '../ProblemEntryPage.css';

const ProblemEntryPage = () => {
  const GRID_SIZE = 9; // 3x3 grid
  const navigate = useNavigate();
  const [currentPosition, setCurrentPosition] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [urlInput, setUrlInput] = useState('');
  const [gridCells, setGridCells] = useState(Array(GRID_SIZE).fill(null));
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 6; // Updated to 6 pages

  // Open the URL input modal
  const openUrlModal = () => {
    setIsModalOpen(true);
  };

  // Close the URL input modal
  const closeUrlModal = () => {
    setIsModalOpen(false);
    setUrlInput('');
  };

  // Handle URL submission
  const submitUrl = () => {
    if (urlInput.trim()) {
      // Update the grid cells array
      const newGridCells = [...gridCells];
      newGridCells[currentPosition] = urlInput.trim();
      setGridCells(newGridCells);
      
      // Move to the next position
      setCurrentPosition(prevPosition => prevPosition + 1);
      
      // Close the modal
      closeUrlModal();
      
      // Navigate to ChatPage
      navigate('/chat', { state: { url: urlInput.trim() } });
    }
  };

  // Handle keyboard events
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      submitUrl();
    }
  };

  // Handle pagination
  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    // Reset grid for demo purposes
    setGridCells(Array(GRID_SIZE).fill(null));
    setCurrentPosition(0);
  };

  // Navigate to previous page
  const goToPrevPage = () => {
    if (currentPage > 1) {
      handlePageChange(currentPage - 1);
    }
  };

  // Navigate to next page
  const goToNextPage = () => {
    if (currentPage < totalPages) {
      handlePageChange(currentPage + 1);
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
        onClick={() => handlePageChange(1)}
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
              onClick={() => handlePageChange(i)}
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
            onClick={() => handlePageChange(i)}
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
          onClick={() => handlePageChange(totalPages)}
        >
          {totalPages}
        </button>
      );
    }
    
    return paginationItems;
  };

  return (
    <div className="url-grid-page">
      <Navbar />
      
      <div className="url-grid-wrapper">
        <div className="url-grid-container">
          <div className="url-grid-header">
            <h2>Enter the Project URL's</h2>
            <div className="url-grid-page-indicator">Page {currentPage} of {totalPages}</div>
          </div>
          
          <div className="url-grid">
            {Array(GRID_SIZE).fill(null).map((_, index) => (
              <div className="url-grid-cell" key={index}>
                {index === currentPosition && currentPosition < GRID_SIZE ? (
                  <button className="url-grid-add-button" onClick={openUrlModal}>
                    <span className="plus-icon">+</span>
                  </button>
                ) : gridCells[index] ? (
                  <div className="url-grid-url-display">
                    <div className="url-grid-url-text">{gridCells[index]}</div>
                    <div className="url-grid-url-favicon">
                      <div className="favicon-placeholder"></div>
                    </div>
                  </div>
                ) : null}
              </div>
            ))}
          </div>
          
          {/* Enhanced Pagination */}
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
          if (e.target.className === 'url-grid-modal') closeUrlModal();
        }}>
          <div className="url-grid-modal-content">
            <h3>Add Project URL</h3>
            <div className="url-grid-form-group">
              <input 
                type="url" 
                placeholder="Enter project URL" 
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                onKeyPress={handleKeyPress}
                autoFocus
                required 
              />
            </div>
            <div className="url-grid-buttons">
              <button className="url-grid-btn url-grid-btn-cancel" onClick={closeUrlModal}>Cancel</button>
              <button className="url-grid-btn url-grid-btn-submit" onClick={submitUrl}>Submit</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProblemEntryPage;
