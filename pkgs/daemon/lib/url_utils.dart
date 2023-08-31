/// This needs to exist because by default Uri.host doesn't remove subdomains.
/// So if you want just the domain name, you have to split at the '.' character
/// and then take the last two items.
String getDomainFromHost(String host) {
  final rawUrlParts = host.split('.');
  return '${rawUrlParts[rawUrlParts.length - 2]}.${rawUrlParts[rawUrlParts.length - 1]}';
}
