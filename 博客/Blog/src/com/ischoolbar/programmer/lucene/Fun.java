package com.ischoolbar.programmer.lucene;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import com.ischoolbar.programmer.entity.Blog;
import com.ischoolbar.programmer.entity.PageBean;
import com.ischoolbar.programmer.util.DateUtil;
import com.ischoolbar.programmer.service.impl.BlogServiceImpl;;

public class Fun {

	public static void main(String[] args) throws IOException {
//		try {
//			addIndex(new Blog());
//		} catch (Exception e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
		
	}
	
	public  void addIndex(Blog blog)throws Exception{
		IndexWriter writer=getWriter();
		Document doc=new Document();
		doc.add(new StringField("id",String.valueOf(blog.getId()),Field.Store.YES));
		doc.add(new TextField("title",blog.getTitle(),Field.Store.YES));
		doc.add(new StringField("releaseDate",DateUtil.formatDate(new Date(), "yyyy-MM-dd"),Field.Store.YES));
//		doc.add(new TextField("content",blog.getContentNoTag(),Field.Store.YES));
		writer.addDocument(doc);
		writer.close();
	}
	
	private static IndexWriter getWriter()throws Exception{
		Directory dir = null;
		dir=FSDirectory.open(Paths.get("C://lucene")); //指定索引库的存放位置
		SmartChineseAnalyzer analyzer=new SmartChineseAnalyzer();  //指定一个标准分析器，对文档内容分析
		IndexWriterConfig iwc=new IndexWriterConfig(analyzer);
		IndexWriter writer=new IndexWriter(dir, iwc);
		return writer;
	}

}
