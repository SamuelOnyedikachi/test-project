class ContactPermission {
  const ContactPermission({
    required this.canViewLiveLocation,
    required this.canViewRouteHistory,
    required this.canViewBattery,
    required this.canViewMedicalInfo,
    required this.canReceiveSos,
  });

  const ContactPermission.guardian()
    : canViewLiveLocation = true,
      canViewRouteHistory = true,
      canViewBattery = true,
      canViewMedicalInfo = false,
      canReceiveSos = true;

  const ContactPermission.responder()
    : canViewLiveLocation = true,
      canViewRouteHistory = true,
      canViewBattery = true,
      canViewMedicalInfo = true,
      canReceiveSos = true;

  final bool canViewLiveLocation;
  final bool canViewRouteHistory;
  final bool canViewBattery;
  final bool canViewMedicalInfo;
  final bool canReceiveSos;

  Map<String, Object?> toJson() {
    return {
      'canViewLiveLocation': canViewLiveLocation,
      'canViewRouteHistory': canViewRouteHistory,
      'canViewBattery': canViewBattery,
      'canViewMedicalInfo': canViewMedicalInfo,
      'canReceiveSos': canReceiveSos,
    };
  }
}
