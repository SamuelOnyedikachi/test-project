class LocalClockFormatter {
  const LocalClockFormatter._();

  static String greetingFor(DateTime localTime) {
    if (localTime.hour < 12) return 'Good morning';
    if (localTime.hour < 17) return 'Good afternoon';
    return 'Good evening';
  }

  static String timeZoneLabel(DateTime localTime) {
    final offset = localTime.timeZoneOffset;
    final sign = offset.isNegative ? '-' : '+';
    final hours = offset.inHours.abs().toString().padLeft(2, '0');
    final minutes = (offset.inMinutes.abs() % 60).toString().padLeft(2, '0');
    return '${localTime.timeZoneName} (UTC$sign$hours:$minutes)';
  }
}
