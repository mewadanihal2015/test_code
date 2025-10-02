// Random VFX Settings Generator
public class VFXSettings
{
    public float ParticleSize;
    public float EmissionRate;
    public float Lifetime;
    public float GlowIntensity;
    public UnityEngine.Color Color;

    public static VFXSettings GenerateRandom()
    {
        System.Random rand = new System.Random();
        return new VFXSettings
        {
            ParticleSize   = (float)(0.1 + rand.NextDouble() * 2.0),     // 0.1 - 2.1
            EmissionRate   = rand.Next(10, 200),                         // 10 - 200
            Lifetime       = (float)(0.5 + rand.NextDouble() * 5.0),     // 0.5 - 5.5
            GlowIntensity  = (float)(rand.NextDouble() * 3.0),           // 0 - 3
            Color          = new UnityEngine.Color(
                                (float)rand.NextDouble(),
                                (float)rand.NextDouble(),
                                (float)rand.NextDouble(),
                                1f)                                     // Random RGB
        };
    }
}

// Example usage:
VFXSettings vfx = VFXSettings.GenerateRandom();
Debug.Log($"Generated VFX - Size:{vfx.ParticleSize}, Rate:{vfx.EmissionRate}, Lifetime:{vfx.Lifetime}, Glow:{vfx.GlowIntensity}, Color:{vfx.Color}");
