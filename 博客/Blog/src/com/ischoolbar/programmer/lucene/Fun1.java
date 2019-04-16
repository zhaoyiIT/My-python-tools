package com.ischoolbar.programmer.lucene;
import org.jsoup.Jsoup;

public class Fun1 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String html = "<p sdf>哈哈哈哈的风景按时给非递归</p><p sdf>哈哈哈哈的风ddd景按时给非递归</p>";
				
		parse(html);	
	}
	
	public static void parse(String html){
		String new_textString = Jsoup.parse(html).text();
		System.out.println(new_textString);
	}

}
