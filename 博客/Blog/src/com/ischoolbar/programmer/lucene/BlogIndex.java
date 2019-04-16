package com.ischoolbar.programmer.lucene;

import java.io.StringReader;
import java.nio.file.Paths;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;

import org.apache.commons.lang.StringEscapeUtils;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.BooleanClause;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.highlight.Fragmenter;
import org.apache.lucene.search.highlight.Highlighter;
import org.apache.lucene.search.highlight.QueryScorer;
import org.apache.lucene.search.highlight.SimpleHTMLFormatter;
import org.apache.lucene.search.highlight.SimpleSpanFragmenter;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import com.ischoolbar.programmer.entity.Blog;
import com.ischoolbar.programmer.util.DateUtil;
import com.ischoolbar.programmer.util.StringUtil;

/**
 * 博客索引类
 * @author Administrator
 *
 */
public class BlogIndex {

	private Directory dir=null;
	

	/**
	 * 获取IndexWriter实例
	 * @return
	 * @throws Exception
	 */
	private IndexWriter getWriter()throws Exception{
		
		dir=FSDirectory.open(Paths.get("C://lucene")); //指定索引库的存放位置
		SmartChineseAnalyzer analyzer=new SmartChineseAnalyzer();  //指定一个标准分析器，对文档内容分析
		IndexWriterConfig iwc=new IndexWriterConfig(analyzer);
		IndexWriter writer=new IndexWriter(dir, iwc);
		return writer;
	}
	
	/**
	 * 添加博客索引
	 * @param blog
	 */
	public void addIndex(Blog blog)throws Exception{
		IndexWriter writer=getWriter();
		Document doc=new Document();
		doc.add(new StringField("id",String.valueOf(blog.getId()),Field.Store.YES));
		doc.add(new TextField("title",blog.getTitle(),Field.Store.YES));
		doc.add(new StringField("releaseDate",DateUtil.formatDate(new Date(), "yyyy-MM-dd"),Field.Store.YES));
		doc.add(new TextField("content",blog.getContentNoTag(),Field.Store.YES));
		writer.addDocument(doc);
		writer.close();
	}
	
	/**
	 * 更新博客索引
	 * @param blog
	 * @throws Exception
	 */
	public void updateIndex(Blog blog)throws Exception{
		IndexWriter writer=getWriter();
		Document doc=new Document();
		doc.add(new StringField("id",String.valueOf(blog.getId()),Field.Store.YES));
		doc.add(new TextField("title",blog.getTitle(),Field.Store.YES));
		doc.add(new StringField("releaseDate",DateUtil.formatDate(new Date(), "yyyy-MM-dd"),Field.Store.YES));
		doc.add(new TextField("content",blog.getContentNoTag(),Field.Store.YES));
		writer.updateDocument(new Term("id", String.valueOf(blog.getId())), doc);
		writer.close();
	}
	
	/**
	 * 删除指定博客的索引
	 * @param blogId
	 * @throws Exception
	 */
	public void deleteIndex(String blogId)throws Exception{
		IndexWriter writer=getWriter();
		writer.deleteDocuments(new Term("id",blogId));
		writer.forceMergeDeletes(); // 强制删除
		writer.commit();
		writer.close();
	}
	
	/**
	 * 查询博客信息
	 * @param q 查询关键字
	 * @return.
	 * @throws Exception
	 */
	public List<Blog> searchBlog(String q)throws Exception{
		dir=FSDirectory.open(Paths.get("C://lucene"));	 // 打开索引库文件
		IndexReader reader = DirectoryReader.open(dir);	// 创建索引读取器对象	
		IndexSearcher is=new IndexSearcher(reader);		// 创建索引搜索器对象
		
		BooleanQuery.Builder booleanQuery = new BooleanQuery.Builder(); 
		SmartChineseAnalyzer analyzer=new SmartChineseAnalyzer();
		QueryParser parser=new QueryParser("title",analyzer);
		Query query=parser.parse(q);	//得到用来查询title的查询器
		QueryParser parser2=new QueryParser("content",analyzer);
		Query query2=parser2.parse(q);  //得到用来查询content的查询器
		//booleanQuery是一个查询器，包含了查询title、查询content
		booleanQuery.add(query,BooleanClause.Occur.SHOULD);
		booleanQuery.add(query2,BooleanClause.Occur.SHOULD);
		
		//执行查询，参数1是查询对象，参数2是查询结果返回的最大值
		TopDocs hits=is.search(booleanQuery.build(), 100);
		
		/*
		 *	给查询关键词高亮显示 
		 */
		QueryScorer scorer=new QueryScorer(query);  
		Fragmenter fragmenter = new SimpleSpanFragmenter(scorer);  
		SimpleHTMLFormatter simpleHTMLFormatter=new SimpleHTMLFormatter("<b><font color='red'>","</font></b>");
		Highlighter highlighter=new Highlighter(simpleHTMLFormatter, scorer);
		highlighter.setTextFragmenter(fragmenter);  
		
		
		List<Blog> blogList=new LinkedList<Blog>();
		for(ScoreDoc scoreDoc:hits.scoreDocs){   //hits.scoreDocs存储了document对象的id
			Document doc=is.doc(scoreDoc.doc);    //根据document的id找到document对象
			/*
			 *	从查询出来的对象中，取出title，content信息，封装到blog对象 ，将blog对象添加到列表，返回
			 **/
			Blog blog=new Blog();
			blog.setId(Integer.parseInt(doc.get(("id"))));
			blog.setReleaseDateStr(doc.get(("releaseDate")));
			String title=doc.get("title");
			String content=StringEscapeUtils.escapeHtml(doc.get("content"));
			if(title!=null){
				TokenStream tokenStream = analyzer.tokenStream("title", new StringReader(title));
				String hTitle=highlighter.getBestFragment(tokenStream, title);
				if(StringUtil.isEmpty(hTitle)){
					blog.setTitle(title);
				}else{
					blog.setTitle(hTitle);					
				}
			}
			if(content!=null){
				TokenStream tokenStream = analyzer.tokenStream("content", new StringReader(content)); 
				String hContent=highlighter.getBestFragment(tokenStream, content);
				if(StringUtil.isEmpty(hContent)){
					if(content.length()<=200){
						blog.setContent(content);
					}else{
						blog.setContent(content.substring(0, 200));						
					}
				}else{
					blog.setContent(hContent);					
				}
			}
			blogList.add(blog);
		}
		return blogList;
	}
}
