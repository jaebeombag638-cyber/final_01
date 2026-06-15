import { Routes, Route } from 'react-router-dom';

const Home = () => <div className="p-6 font-bold text-2xl text-blue-600">BuildBack 홈 화면</div>;
const PostList = () => <div className="p-6">커뮤니티 목록 조회 화면</div>;
const PostDetail = () => <div className="p-6">커뮤니티 상세 조회 화면</div>;
const PostWrite = () => <div className="p-6">커뮤니티 작성/수정 화면</div>;

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/posts" element={<PostList />} />
      <Route path="/posts/:post_id" element={<PostDetail />} />
      <Route path="/posts/write" element={<PostWrite />} />
    </Routes>
  );
}

export default App;