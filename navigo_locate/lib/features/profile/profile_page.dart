import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../../shared/widgets/fynder_widgets.dart';
import 'profile_provider.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  late final TextEditingController _nameController;
  bool _saved = false;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(
      text: context.read<ProfileProvider>().name,
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    final image = await ImagePicker().pickImage(
      source: ImageSource.gallery,
      imageQuality: 88,
      maxWidth: 1200,
    );
    if (image == null || !mounted) return;
    context.read<ProfileProvider>().selectGalleryImage(
      await image.readAsBytes(),
    );
  }

  void _save() {
    context.read<ProfileProvider>().saveName(_nameController.text);
    setState(() => _saved = true);
    Future<void>.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _saved = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    final profile = context.watch<ProfileProvider>();
    final cardColor = Theme.of(context).cardColor;

    return Scaffold(
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) => SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 23),
            child: ConstrainedBox(
              constraints: BoxConstraints(minHeight: constraints.maxHeight),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 24),
                  const FynderHeader(),
                  const SizedBox(height: 38),
                  Row(
                    children: [
                      _RoundBackButton(onTap: () => Navigator.pop(context)),
                      const SizedBox(width: 16),
                      const Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Edit Profile',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          SizedBox(height: 3),
                          Text(
                            'Update your profile information',
                            style: TextStyle(
                              fontSize: 11,
                              color: Color(0xFF64789F),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 38),
                  _ProfileCard(
                    color: cardColor,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Choose Avatar',
                          style: TextStyle(fontWeight: FontWeight.w800),
                        ),
                        const SizedBox(height: 5),
                        const Text(
                          'Select an avatar that represents you',
                          style: TextStyle(
                            fontSize: 11,
                            color: Color(0xFF64789F),
                          ),
                        ),
                        const SizedBox(height: 31),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: List.generate(4, (index) {
                            final selected =
                                profile.galleryImage == null &&
                                profile.avatarIndex == index;
                            return GestureDetector(
                              onTap: () => context
                                  .read<ProfileProvider>()
                                  .selectAvatar(index),
                              child: Stack(
                                clipBehavior: Clip.none,
                                children: [
                                  ProfileAvatar(index: index, size: 56),
                                  if (selected)
                                    const Positioned(
                                      right: -4,
                                      top: -6,
                                      child: CircleAvatar(
                                        radius: 12,
                                        backgroundColor: Color(0xFF3478F6),
                                        child: Icon(
                                          Icons.check,
                                          size: 16,
                                          color: Colors.white,
                                        ),
                                      ),
                                    ),
                                ],
                              ),
                            );
                          }),
                        ),
                        const SizedBox(height: 27),
                        TextButton(
                          onPressed: _pickImage,
                          style: TextButton.styleFrom(padding: EdgeInsets.zero),
                          child: const Text('Choose from gallery'),
                        ),
                      ],
                    ),
                  ),
                  if (profile.galleryImage != null) ...[
                    const SizedBox(height: 26),
                    AspectRatio(
                      aspectRatio: 1,
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(2),
                        child: Image.memory(
                          profile.galleryImage!,
                          fit: BoxFit.cover,
                        ),
                      ),
                    ),
                  ],
                  const SizedBox(height: 30),
                  _ProfileCard(
                    color: cardColor,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Your Name',
                          style: TextStyle(fontWeight: FontWeight.w800),
                        ),
                        const SizedBox(height: 5),
                        const Text(
                          'This is how others will see you',
                          style: TextStyle(
                            fontSize: 11,
                            color: Color(0xFF64789F),
                          ),
                        ),
                        const SizedBox(height: 22),
                        TextField(
                          controller: _nameController,
                          onChanged: (_) {
                            if (_saved) setState(() => _saved = false);
                          },
                          decoration: const InputDecoration(
                            hintText: 'Your name',
                          ),
                        ),
                        const SizedBox(height: 24),
                        SizedBox(
                          width: double.infinity,
                          height: 61,
                          child: ElevatedButton.icon(
                            onPressed: _save,
                            icon: _saved
                                ? const SizedBox.shrink()
                                : const Icon(Icons.save_outlined, size: 21),
                            label: Text(
                              _saved ? 'Changes Saved!' : 'Save Changes',
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 52),
                  const ControlFooter(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _ProfileCard extends StatelessWidget {
  const _ProfileCard({required this.color, required this.child});
  final Color color;
  final Widget child;

  @override
  Widget build(BuildContext context) => Container(
    width: double.infinity,
    padding: const EdgeInsets.fromLTRB(24, 23, 24, 18),
    decoration: BoxDecoration(
      color: color,
      borderRadius: BorderRadius.circular(16),
      boxShadow: Theme.of(context).brightness == Brightness.light
          ? const [
              BoxShadow(
                color: Color(0x0D000000),
                blurRadius: 18,
                offset: Offset(0, 8),
              ),
            ]
          : null,
    ),
    child: child,
  );
}

class _RoundBackButton extends StatelessWidget {
  const _RoundBackButton({required this.onTap});
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Material(
    color: Theme.of(context).cardColor,
    shape: const CircleBorder(),
    elevation: Theme.of(context).brightness == Brightness.light ? 1 : 0,
    child: InkWell(
      onTap: onTap,
      customBorder: const CircleBorder(),
      child: const SizedBox(
        width: 34,
        height: 34,
        child: Icon(Icons.chevron_left, size: 25),
      ),
    ),
  );
}
