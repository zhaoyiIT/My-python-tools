package com.ischoolbar.programmer.service;

import com.ischoolbar.programmer.entity.Blogger;

/**
 * ����Service�ӿ�
 * @author java1234_С��
 *
 */
public interface BloggerService {

	/**
	 * ��ѯ������Ϣ
	 * @return
	 */
	public Blogger find();
	
	/**
	 * ͨ���û�����ѯ�û�
	 * @param userName
	 * @return
	 */
	public Blogger getByUserName(String userName);
	
	/**
	 * ���²�����Ϣ
	 * @param blogger
	 * @return
	 */
	public Integer update(Blogger blogger);
}
