String getDomainFromHost(String host) {
  final rawUrlParts = host.split('.');
  return '${rawUrlParts[rawUrlParts.length - 2]}.${rawUrlParts[rawUrlParts.length - 1]}';
}
