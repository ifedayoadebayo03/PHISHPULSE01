"""
WHOIS lookup service for domain intelligence.
"""

import whois
import socket
import dns.resolver
from typing import Dict, Optional
from datetime import datetime


class WHOISLookup:
    """WHOIS and DNS lookup service."""
    
    def lookup(self, domain: str) -> Dict:
        """
        Perform WHOIS lookup for domain.
        
        Returns:
            Dict with domain registration info
        """
        result = {
            "domain": domain,
            "registrar": None,
            "creation_date": None,
            "expiration_date": None,
            "name_servers": [],
            "privacy_protected": False,
            "domain_age_days": None,
            "dns_records": {},
            "error": None
        }
        
        try:
            # WHOIS lookup
            w = whois.whois(domain)
            
            result["registrar"] = w.registrar
            result["name_servers"] = w.name_servers if isinstance(w.name_servers, list) else [w.name_servers]
            
            # Handle creation date (can be list or single date)
            creation = w.creation_date
            if isinstance(creation, list):
                creation = creation[0]
            result["creation_date"] = creation.isoformat() if creation else None
            
            # Handle expiration date
            expiration = w.expiration_date
            if isinstance(expiration, list):
                expiration = expiration[0]
            result["expiration_date"] = expiration.isoformat() if expiration else None
            
            # Calculate domain age
            if creation:
                age = datetime.utcnow() - creation
                result["domain_age_days"] = age.days
            
            # Check for privacy protection
            if w.name_servers:
                privacy_keywords = ['privacy', 'whoisguard', 'protected', 'redacted']
                name_server_str = ' '.join(str(ns).lower() for ns in result["name_servers"] if ns)
                result["privacy_protected"] = any(kw in name_server_str for kw in privacy_keywords)
            
            # DNS records
            result["dns_records"] = self._get_dns_records(domain)
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _get_dns_records(self, domain: str) -> Dict:
        """Get DNS records for domain."""
        records = {
            "a_records": [],
            "mx_records": [],
            "txt_records": [],
            "ns_records": []
        }
        
        try:
            # A records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                records["a_records"] = [str(rdata) for rdata in answers]
            except Exception:
                pass
            
            # MX records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                records["mx_records"] = [str(rdata.exchange) for rdata in answers]
            except Exception:
                pass
            
            # TXT records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                records["txt_records"] = [str(rdata) for rdata in answers]
            except Exception:
                pass
            
            # NS records
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                records["ns_records"] = [str(rdata) for rdata in answers]
            except Exception:
                pass
            
        except Exception:
            pass
        
        return records
    
    def get_ssl_info(self, domain: str, port: int = 443) -> Dict:
        """Get SSL certificate information."""
        import ssl
        import certifi
        
        result = {
            "has_ssl": False,
            "issuer": None,
            "subject": None,
            "not_before": None,
            "not_after": None,
            "serial_number": None,
            "san": [],
            "error": None
        }
        
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    result["has_ssl"] = True
                    result["issuer"] = cert.get("issuer")
                    result["subject"] = cert.get("subject")
                    result["not_before"] = cert.get("notBefore")
                    result["not_after"] = cert.get("notAfter")
                    result["serial_number"] = cert.get("serialNumber")
                    result["san"] = cert.get("subjectAltName", [])
                    result["cipher"] = cipher[0] if cipher else None
                    
        except Exception as e:
            result["error"] = str(e)
        
        return result
