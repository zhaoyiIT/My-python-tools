package com.ischoolbar.programmer.lucene;
import org.jsoup.Jsoup;

public class Fun1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String html = "<p sdf>���������ķ羰��ʱ���ǵݹ�</p><p sdf>���������ķ�ddd����ʱ���ǵݹ�</p>";
				
		parse(html);	
	}
	
	public static void parse(String html){
		String new_textString = Jsoup.parse(html).text();
		System.out.println(new_textString);
	}

}
