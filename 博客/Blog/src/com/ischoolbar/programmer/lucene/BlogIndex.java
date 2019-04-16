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
 * ����������
 * @author Administrator
 *
 */
public class BlogIndex {

	private Directory dir=null;
	

	/**
	 * ��ȡIndexWriterʵ��
	 * @return
	 * @throws Exception
	 */
	private IndexWriter getWriter()throws Exception{
		
		dir=FSDirectory.open(Paths.get("C://lucene")); //ָ��������Ĵ��λ��
		SmartChineseAnalyzer analyzer=new SmartChineseAnalyzer();  //ָ��һ����׼�����������ĵ����ݷ���
		IndexWriterConfig iwc=new IndexWriterConfig(analyzer);
		IndexWriter writer=new IndexWriter(dir, iwc);
		return writer;
	}
	
	/**
	 * ��Ӳ�������
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
	 * ���²�������
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
	 * ɾ��ָ�����͵�����
	 * @param blogId
	 * @throws Exception
	 */
	public void deleteIndex(String blogId)throws Exception{
		IndexWriter writer=getWriter();
		writer.deleteDocuments(new Term("id",blogId));
		writer.forceMergeDeletes(); // ǿ��ɾ��
		writer.commit();
		writer.close();
	}
	
	/**
	 * ��ѯ������Ϣ
	 * @param q ��ѯ�ؼ���
	 * @return.
	 * @throws Exception
	 */
	public List<Blog> searchBlog(String q)throws Exception{
		dir=FSDirectory.open(Paths.get("C://lucene"));	 // ���������ļ�
		IndexReader reader = DirectoryReader.open(dir);	// ����������ȡ������	
		IndexSearcher is=new IndexSearcher(reader);		// ������������������
		
		BooleanQuery.Builder booleanQuery = new BooleanQuery.Builder(); 
		SmartChineseAnalyzer analyzer=new SmartChineseAnalyzer();
		QueryParser parser=new QueryParser("title",analyzer);
		Query query=parser.parse(q);	//�õ�������ѯtitle�Ĳ�ѯ��
		QueryParser parser2=new QueryParser("content",analyzer);
		Query query2=parser2.parse(q);  //�õ�������ѯcontent�Ĳ�ѯ��
		//booleanQuery��һ����ѯ���������˲�ѯtitle����ѯcontent
		booleanQuery.add(query,BooleanClause.Occur.SHOULD);
		booleanQuery.add(query2,BooleanClause.Occur.SHOULD);
		
		//ִ�в�ѯ������1�ǲ�ѯ���󣬲���2�ǲ�ѯ������ص����ֵ
		TopDocs hits=is.search(booleanQuery.build(), 100);
		
		/*
		 *	����ѯ�ؼ��ʸ�����ʾ 
		 */
		QueryScorer scorer=new QueryScorer(query);  
		Fragmenter fragmenter = new SimpleSpanFragmenter(scorer);  
		SimpleHTMLFormatter simpleHTMLFormatter=new SimpleHTMLFormatter("<b><font color='red'>","</font></b>");
		Highlighter highlighter=new Highlighter(simpleHTMLFormatter, scorer);
		highlighter.setTextFragmenter(fragmenter);  
		
		
		List<Blog> blogList=new LinkedList<Blog>();
		for(ScoreDoc scoreDoc:hits.scoreDocs){   //hits.scoreDocs�洢��document�����id
			Document doc=is.doc(scoreDoc.doc);    //����document��id�ҵ�document����
			/*
			 *	�Ӳ�ѯ�����Ķ����У�ȡ��title��content��Ϣ����װ��blog���� ����blog������ӵ��б�����
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
