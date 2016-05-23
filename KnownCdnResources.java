package com.shunra.analyzerexpress.protocols.http.cdn;

import java.util.HashMap;
import java.util.Map;

/**
 * Internal class used be Cdn.java
 * Figure out if a resource is a CDN based on hostname or server header
 * This is called repeatedly when we lookup DNS records, checking each DNS entry for a possible match
 *  * 
 * @author Les Murphy
 *
 */


public class KnownCdnResources {

	private static final Map<String, String> cdnMap;
	private static final Map<String, String> cdnServerHeaderMap;
	
	// see http://www.cdnplanet.com/blog/better-cdn-finder/
	// and http://www.cdnplanet.com/tools/cdnfinder/

	// TODO - see if any lookups other than the trailing 2 nodes are worth detecting.

	// TODO FLAG NO CDN?  Do we want these to be CDN or not?
	// https://ajax.cloudflare.com/cdn-cgi/nexp/dok3v=e9627cd26a/cloudflare.min.js
	// https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.7.1/modernizr.min.js
	
	// TODO - is it of any value to detect non CDN external services such as https://pantheon.io/
	// headers  X-Pantheon-Endpoint: 126e0b6f-345d-495d-8b8a-793a55fec3a1  X-Pantheon-Styx-Hostname: styx112b8753
	
	// Note that lookups CAN return the same IP for multiple CDN servers - anycast!
	//   e.g. see https://asm.ca.com/en/ping.php for www.swoodoo.com (fastlybgp.r9cdn.net)
	
	// see also:  https://github.com/WPO-Foundation/webpagetest/blob/2b528f848064dc282a07691ffdd2256d78e325c6/agent/browser/ie/pagetest/cdn.h

	 static {
		 cdnServerHeaderMap = new HashMap<String, String>();
		 cdnServerHeaderMap.put("Akamai", "Akamai");
		 cdnServerHeaderMap.put("cloudflare", "Cloudflare");
		 cdnServerHeaderMap.put("ECS", "EdgeCast");
		 cdnServerHeaderMap.put("ECAcc", "EdgeCast");
		 cdnServerHeaderMap.put("ECD", "EdgeCast");
		 cdnServerHeaderMap.put("NetDNA", "MaxCDN Enterprise");  // https://www.maxcdn.com/blog/netdna-maxcdn-enterprise/  NetDNA now MaxCDN Enterprise
		 cdnServerHeaderMap.put("Airee", "Airee");
		 cdnServerHeaderMap.put("ReSRC", "ReSRC.it");
		 cdnServerHeaderMap.put("Zenedge", "Zenedge");
		 cdnServerHeaderMap.put("Caspowa", "Caspowa");
		 cdnServerHeaderMap.put("SurgeCDN", "Surge");
	 }
	
	 static {
			cdnMap = new HashMap<String, String>();
			cdnMap.put("akamaitechnologies.com", "Akamai");
			cdnMap.put("afxcdn.net", "afxcdn.net");
			cdnMap.put("akadns.net", "Akamai");
			cdnMap.put("akamai.net", "Akamai");
			cdnMap.put("akamaihd.net", "Akamai");  // from WPT
			cdnMap.put("akamaiedge.net", "Akamai");
			cdnMap.put("alicdn.com", "Alibaba CDN"); // China
			cdnMap.put("anankecdn.com.br", "Ananke");
			cdnMap.put("att-dsa.net", "AT&T");
			// cdnMap.put("ay1.b.yahoo.com", "Yahoo");
			cdnMap.put("azioncdn.net", "Azion");
			cdnMap.put("azioncdn.com", "Azion");  // From WPT
			cdnMap.put("azion.net", "Azion");  // From WPT
			cdnMap.put("bluehatnetwork.com", "Blue Hat Network");
			cdnMap.put("bo.lt", "BO.LT");
			cdnMap.put("c3cache.net", "ChinaCache");
			cdnMap.put("c3cdn.net", "ChinaCache");
			cdnMap.put("caspowa.com", "Caspowa");  
			cdnMap.put("cdn77.org", "CDN77");  // see https://www.cdn77.com/  sample test site http://www.ivoox.com/.  Response header  Server: CDN77-Turbo
			cdnMap.put("cdn77.net", "CDN77");
			cdnMap.put("cdnsun.net", "CDNsun"); // From WPT
			cdnMap.put("cachefly.net", "Cachefly");
			cdnMap.put("cap-mii.net", "Mirror Image");
			cdnMap.put("ccgslb.com", "ChinaCache");
			cdnMap.put("ccgslb.net", "ChinaCache");
			cdnMap.put("bitgravity.com", "Bitgravity");
			// cdnMap.put("telefonica.com", "Telefonica");
			
			cdnMap.put("cdngc.net", "CDNetworks");
			cdnMap.put("chinacache.net", "ChinaCache");

			// cdnMap.put("clients.turbobytes.com", "Turbobytes");

			// note Cloudflare also has response header of Server: cloudflare-nginx
			cdnMap.put("cloudflare.com", "Cloudflare");
			cdnMap.put("cloudfront.net", "Amazon Cloudfront");
			cdnMap.put("cotcdn.net", "Cotendo");
			// from c2.neweggimages.com.cn - root page is www.newegg.com.cn
			// cloudcdn.net hacdn.net
			cdnMap.put("cloudcdn.cn", "CDNetworks"); // Not 100% sure yet ...
			
			cdnMap.put("cubecdn.net", "cubeCDN"); // based in Turkey

			cdnMap.put("edgecastcdn.net", "EdgeCast");  // Verizon acquired EdgeCast in 2013
			cdnMap.put("systemcdn.net", "EdgeCast"); 
			cdnMap.put("transactcdn.net", "EdgeCast");  
			cdnMap.put("v1cdn.net", "EdgeCast");  
			cdnMap.put("v2cdn.net", "EdgeCast");  
			cdnMap.put("v3cdn.net", "EdgeCast");  
			cdnMap.put("v4cdn.net", "EdgeCast");  
			cdnMap.put("v5cdn.net", "EdgeCast");  
			
			cdnMap.put("edgesuite.net", "Akamai");  
			cdnMap.put("edgekey.net", "Akamai");  
			cdnMap.put("srip.net", "Akamai");  
			
			// https://www.fastly.com/network  Network map
			cdnMap.put("fastly.net", "Fastly");
			cdnMap.put("fastlylb.net", "Fastly");  
			cdnMap.put("r9cdn.net", "Fastly");  // fastlybgp.r9cdn.net  for swoodoo.com   Kayak uses Fastly https://www.fastly.com/customers
			
			cdnMap.put("fbcdn.net", "Facebook"); // e.g.cdn.atlassbx.com
			cdnMap.put("fpbns.net", "Level-3"); 
			cdnMap.put("footprint.net", "Level3");
			cdnMap.put("gccdn.cn", "CDNetworks");
			cdnMap.put("gccdn.net", "CDNetworks");
			// cdnMap.put("google.", "Google");
			cdnMap.put("googlesyndication.", "Google");
			cdnMap.put("googleusercontent.com", "Google");

			cdnMap.put("googleapis.com", "Google"); // LLM added for ajax.googleapis.com
			cdnMap.put("ytimg.com", "Google"); // LLM YouTube
			// ytstatic.l.google.com for s.ytimg
			// ytimg.l.google.com for i.ytimg

			// cdnMap.put("gslb.taobao.com", "Taobao");
			// cdnMap.put("gslb.tbcache.com", "Alimama");

			cdnMap.put("taobao.com", "Taobao");
			cdnMap.put("tbcache.com", "Alimama");

			cdnMap.put("hwcdn.net", "Highwinds");
			cdnMap.put("incapdns.net", "Incapsula");  
			cdnMap.put("instacontent.net", "Mirror Image");
			cdnMap.put("insnw.net", "Instart Logic");  
			cdnMap.put("inscname.net", "Instart Logic");  
			cdnMap.put("internapcdn.net", "Internap");
			cdnMap.put("jsdelivr.net", "jsDelivr");  
			cdnMap.put("kxcdn.com", "KeyCDN");
			// cdnMap.put("l.doubleclick.net", "Google");
			cdnMap.put("llnwd.net", "Limelight");
			cdnMap.put("lswcdn.net", "LeaseWeb CDN");
			cdnMap.put("lxdns.com", "ChinaNetCenter");
			cdnMap.put("wscdns.com", "ChinaNetCenter");  
			cdnMap.put("wscloudcdn.com", "ChinaNetCenter");  
			cdnMap.put("ourwebpic.com", "ChinaNetCenter");  
			cdnMap.put("mncdn.com", "Medianova");  
			cdnMap.put("mncdn.net", "Medianova");  
			cdnMap.put("mncdn.org", "Medianova");  
			
			
			cdnMap.put("mirror-image.net", "Mirror Image");
			cdnMap.put("netdna-cdn.com", "MaxCDN Enterprise");  
			cdnMap.put("netdna-ssl.com", "MaxCDN Enterprise");
			cdnMap.put("netdna.com", "MaxCDN Enterprise");
			cdnMap.put("ngenix.net", "NGENIX");  
			
			
			cdnMap.put("panthercdn.com", "CDNetworks");
			cdnMap.put("pagerain.net", "PageRain");  
			cdnMap.put("reblaze.com", "Reblaze");
			cdnMap.put("revcn.net", "Rev Software"); 
			cdnMap.put("revdn.net", "Rev Software"); 
			
			cdnMap.put("rhocdn.net", "Reblaze");  // Security Gateways, CDN
			cdnMap.put("rncdn1.com", "Reflected Networks");
			// cdn11.contentabc.com --> vip0x04e.ssl.rncdn5.com reflected networks
			// CDN!
			cdnMap.put("rncdn5.com", "Reflected Networks"); // LLM added. TODO need
															// a better pattern
															// matcher for this!
			cdnMap.put("simplecdn.net", "Simple CDN");
			cdnMap.put("squixacdn.net", "section.io");  	// eg. https://www.thrifty.com.au/ lookup has san1.au5004.squixacdn.net
			cdnMap.put("squixa.net", "section.io");  
			cdnMap.put("swiftcdn1.com", "SwiftCDN");
			cdnMap.put("systemcdn.net", "EdgeCast");
			cdnMap.put("vo.msecnd.net", "Windows Azure"); // vo.msecnd.net

			cdnMap.put("voxcdn.net", "Voxel");
			cdnMap.put("worldcdn.net", "OnApp");  
			cdnMap.put("worldssl1.net", "OnApp");  
			cdnMap.put("yottaa.net", "Yotta");  
			cdnMap.put("zenedge.net", "Zenedge");  
			
			
			cdnMap.put("zetacdn.net", "EdgeCast");  // Edgecast now part of Verizon (acquired in 2013 for > 350M)
			// cdnMap.put("yimg.", "Yahoo");
			// cdnMap.put("youtube.", "Google");
		}

		// Note - use this website to see how a host resolves worldwide
		// CA App Synthetic Monitor Ping test
		// https://asm.ca.com/en/ping.php

		// Java build in DNS routines are too limited, it appears.

		// The basic CNAME resolve will work in Java, but it generates a lot of
		// lookups to the DNS server ...

		// This is the solution:
		// http://sourceforge.net/projects/dnsjava/
		// http://www.dnsjava.org/download/ -- org.xbill.dns_2.1.7.jar
		// try out using test driver dig.java to see how it works ...

	
	 /**
	 * Looks up a hostname in the inventory of known CDNs
	 *  
	 * @param hostname  the hostname to lookup
	 * @return    the CDN name if the hostname is recognized, otherwise null       
	 */
	String CdnLookup(String hostname) {
		String cdnName = null;

		if (hostname.endsWith(".")) {
			// DNS lookup CNAME from the seems to return a trailing period, at least on Windows
			int trailing = hostname.lastIndexOf(".");
			hostname = hostname.substring(0, trailing);

		}

		if (hostname.equals("linkedfastly.contextweb.com"))
			return "Fastly"; // todo research this some more and generalize

		String lastTwoNodesHostname = getLastNodes(hostname);
		if (lastTwoNodesHostname != null)
			cdnName = cdnMap.get(lastTwoNodesHostname);
		return cdnName;
	}


	/**
	 * return the last two nodes, e.g. www-bbc-com.bbc.net.uk -> net.uk
	 * 
	 * @param hostname
	 * @return the last two nodes of the hostname
	 */
	private String getLastNodes(String hostname) {
		// TODO Auto-generated method stub
		int i = hostname.lastIndexOf(".");
		if (i == -1)
			return null;
		int j = hostname.substring(0, i).lastIndexOf(".");
		if (j == -1)
			return hostname; // only two nodes in hostname
		else
			return hostname.substring(j + 1);

	}
	
	
	/**
	 * In some cases we can only figure out the presence of a CDN by looking at the HTTP response "server" header 
	 * @param serverHeaderValue the "server" HTTP response header
	 * @return the CDN name if it can be determined by the header value, otherwise null
	 */
	static String lookupServerHeader(String serverHeaderValue) {
		for (Map.Entry<String, String> entry : cdnServerHeaderMap.entrySet()) {
			 if (serverHeaderValue.contains(entry.getKey()))
			 return entry.getValue();
		}
		
		return null;
		}


	public static String lookupXCacheHeader(String xCacheHeaderValue) {
		if (xCacheHeaderValue.contains("cloudfront"))
			return "Amazon Cloudfront";
		return null;
	}
	}