import React, { useState } from 'react';

function App() {
  const [keyword, setKeyword] = useState('');
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedVideos, setSelectedVideos] = useState([]);
  const [saving, setSaving] = useState(false);
  const [languageFilter, setLanguageFilter] = useState('korean');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const videosPerPage = 50;

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!keyword.trim()) {
      setError('키워드를 입력해주세요.');
      return;
    }

    setLoading(true);
    setError('');
    setVideos([]);
    setSelectedVideos([]);
    setCurrentPage(1);

    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      console.log('API URL:', API_BASE_URL); // 디버깅용
      
      const response = await fetch(`${API_BASE_URL}/search?keyword=${encodeURIComponent(keyword)}&language_filter=${languageFilter}`);
      
      if (!response.ok) {
        throw new Error('검색 중 오류가 발생했습니다.');
      }

      const data = await response.json();
      setVideos(data.videos || []);
      setTotalCount(data.total_count || 0);
    } catch (err) {
      console.error('Search error:', err); // 디버깅용
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 현재 페이지의 비디오들
  const getCurrentPageVideos = () => {
    const startIndex = (currentPage - 1) * videosPerPage;
    const endIndex = startIndex + videosPerPage;
    return videos.slice(startIndex, endIndex);
  };

  const totalPages = Math.ceil(videos.length / videosPerPage);
  const currentPageVideos = getCurrentPageVideos();

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedVideos([...currentPageVideos]);
    } else {
      setSelectedVideos([]);
    }
  };

  const handleSelectVideo = (video, checked) => {
    if (checked) {
      setSelectedVideos([...selectedVideos, video]);
    } else {
      setSelectedVideos(selectedVideos.filter(v => v.id !== video.id));
    }
  };

  const handleSaveSelected = async () => {
    if (selectedVideos.length === 0) {
      setError('저장할 영상을 선택해주세요.');
      return;
    }

    setSaving(true);
    setError('');

    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_BASE_URL}/save-selected`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keyword: keyword,
          selected_videos: selectedVideos
        }),
      });

      if (!response.ok) {
        throw new Error('저장 중 오류가 발생했습니다.');
      }

      const data = await response.json();
      alert(data.message);
      setSelectedVideos([]);
    } catch (err) {
      console.error('Save error:', err); // 디버깅용
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  // 디버깅용 정보 표시
  console.log('App rendered:', {
    API_URL: process.env.REACT_APP_API_URL,
    videosCount: videos.length,
    currentPage,
    totalPages
  });

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
            YouTube 키워드 영상 링크 수집
          </h1>
          
          {/* 디버깅 정보 표시 */}
          <div className="mb-4 p-2 bg-gray-100 text-sm text-gray-600 rounded">
            <p>API URL: {process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'}</p>
            <p>환경: {process.env.NODE_ENV || 'development'}</p>
            <p>배포 시간: {new Date().toLocaleString()}</p>
            <p>빌드 테스트: v2.0</p>
            <p>실제 사용 URL: {process.env.REACT_APP_API_URL ? 'Railway 백엔드' : '로컬 개발'}</p>
          </div>
          
          <form onSubmit={handleSearch} className="mb-6">
            <div className="flex gap-4 mb-4">
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="검색할 키워드를 입력하세요..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <select
                value={languageFilter}
                onChange={(e) => setLanguageFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="korean">한국어 영상 우선</option>
                <option value="all">상관없이 모두</option>
              </select>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? '검색 중...' : '검색'}
              </button>
            </div>
          </form>

          {error && (
            <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-4 text-gray-600">영상을 검색하고 있습니다...</p>
            </div>
          )}

          {videos.length > 0 && (
            <div className="mt-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-800">
                  검색 결과 (총 {totalCount}개 중 {currentPageVideos.length}개 표시)
                </h2>
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      onChange={handleSelectAll}
                      checked={currentPageVideos.length > 0 && selectedVideos.length === currentPageVideos.length}
                      className="w-4 h-4"
                    />
                    <span className="text-sm text-gray-600">현재 페이지 전체선택</span>
                  </label>
                  <button
                    onClick={handleSaveSelected}
                    disabled={saving || selectedVideos.length === 0}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
                  >
                    {saving ? '저장 중...' : `선택된 ${selectedVideos.length}개 구글 시트에 저장`}
                  </button>
                </div>
              </div>
              
              <div className="space-y-3">
                {currentPageVideos.map((video, index) => (
                  <div key={video.id} className="p-4 bg-gray-50 rounded-lg border">
                    <div className="flex items-start gap-3">
                      <input
                        type="checkbox"
                        checked={selectedVideos.some(v => v.id === video.id)}
                        onChange={(e) => handleSelectVideo(video, e.target.checked)}
                        className="w-4 h-4 mt-1"
                      />
                      <div className="flex-1">
                        <div className="flex justify-between items-start mb-2">
                          <span className="text-sm text-gray-600">영상 {(currentPage - 1) * videosPerPage + index + 1}</span>
                          <a
                            href={video.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 hover:text-blue-700 text-sm"
                          >
                            새 창에서 열기
                          </a>
                        </div>
                        <h3 className="font-medium text-gray-800 mb-1 line-clamp-2">
                          {video.title}
                        </h3>
                        <div className="text-sm text-gray-600 mb-2">
                          <span>채널: {video.channel}</span>
                          <span className="mx-2">•</span>
                          <span>조회수: {video.viewCount ? video.viewCount.toLocaleString() : 'N/A'}회</span>
                          <span className="mx-2">•</span>
                          <span>게시일: {new Date(video.publishedAt).toLocaleDateString()}</span>
                        </div>
                        <a
                          href={video.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 break-all text-sm"
                        >
                          {video.url}
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* 페이징 */}
              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-2 mt-6">
                  <button
                    onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                    disabled={currentPage === 1}
                    className="px-3 py-1 bg-gray-200 text-gray-700 rounded disabled:bg-gray-100 disabled:text-gray-400"
                  >
                    이전
                  </button>
                  
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                    <button
                      key={page}
                      onClick={() => setCurrentPage(page)}
                      className={`px-3 py-1 rounded ${
                        currentPage === page
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {page}
                    </button>
                  ))}
                  
                  <button
                    onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                    disabled={currentPage === totalPages}
                    className="px-3 py-1 bg-gray-200 text-gray-700 rounded disabled:bg-gray-100 disabled:text-gray-400"
                  >
                    다음
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;