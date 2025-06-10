import arcade

print(f'Arcade version: {arcade.version.VERSION}')
print('\nArcade attributes:')
attrs = [attr for attr in dir(arcade) if not attr.startswith('_')]
for attr in sorted(attrs):
    print(f'  {attr}')

# Check for particle-related attributes
particle_attrs = [attr for attr in attrs if 'particle' in attr.lower() or 'emitter' in attr.lower()]
print(f'\nParticle-related attributes: {particle_attrs}')

# Check if there are any examples we can run
try:
    import arcade.examples
    print('\nArcade examples module found')
except ImportError:
    print('\nNo arcade examples module')