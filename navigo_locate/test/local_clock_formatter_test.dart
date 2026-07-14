import 'package:flutter_test/flutter_test.dart';
import 'package:navigo_locate/core/utils/local_clock_formatter.dart';

void main() {
  test('greeting changes with local hour', () {
    expect(
      LocalClockFormatter.greetingFor(DateTime(2026, 7, 14, 8)),
      'Good morning',
    );
    expect(
      LocalClockFormatter.greetingFor(DateTime(2026, 7, 14, 14)),
      'Good afternoon',
    );
    expect(
      LocalClockFormatter.greetingFor(DateTime(2026, 7, 14, 20)),
      'Good evening',
    );
  });

  test('timezone label includes UTC offset', () {
    expect(LocalClockFormatter.timeZoneLabel(DateTime.now()), contains('UTC'));
  });
}
